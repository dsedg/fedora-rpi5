#!/usr/bin/env python3
"""Generate a Markdown reference for a kernel .config and its Kconfig help."""

import argparse
from pathlib import Path
import re
import sys


SET_OPTION = re.compile(r"^CONFIG_([A-Za-z0-9_]+)=(.*)$")
UNSET_OPTION = re.compile(r"^# CONFIG_([A-Za-z0-9_]+) is not set$")
CONFIG_DECLARATION = re.compile(r"^\s*(?:menu)?config\s+([A-Za-z0-9_]+)\b")
STRUCTURAL_LINE = re.compile(
    r"^(?:choice|endchoice|menu|endmenu|if|endif|source|rsource|orsource|"
    r"comment|mainmenu)\b"
)
PROMPT_PROPERTY = re.compile(
    r'^(?:bool|tristate|string|int|hex|def_bool|def_tristate)\s+"((?:\\.|[^"\\])*)"'
)
PROMPT_LINE = re.compile(r'^prompt\s+"((?:\\.|[^"\\])*)"')
HELP_PROPERTY = re.compile(r"^(?:help|---help---)\s*$")


def read_config(path):
    options = {}
    config_lines = path.read_text(encoding="utf-8").splitlines()
    for line_number, line in enumerate(config_lines, 1):
        match = SET_OPTION.fullmatch(line)
        if match:
            name, value = match.groups()
        else:
            match = UNSET_OPTION.fullmatch(line)
            if not match:
                continue
            name = match.group(1)
            value = "n"

        if name in options:
            raise ValueError(f"{path}:{line_number}: duplicate CONFIG_{name}")
        options[name] = value

    if not options:
        raise ValueError(f"No CONFIG options found in {path}")
    return options


def collect_options(config_paths):
    options = {}
    for path in config_paths:
        for name, value in read_config(path).items():
            options.setdefault(name, []).append((path.name, value))
    return options


def _append_help(definitions, name, lines, indent):
    while lines and not lines[-1].strip():
        lines.pop()
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        return

    text = "\n".join(line[indent:] if line.strip() else "" for line in lines)
    text = text.strip()
    if text and text not in definitions[name]["help"]:
        definitions[name]["help"].append(text)


def read_kconfig_definitions(source_path, arch):
    definitions = {}
    kconfig_files = []
    for path in source_path.rglob("Kconfig*"):
        if not path.is_file() or not (
            path.name == "Kconfig" or path.name.startswith("Kconfig.")
        ):
            continue
        relative = path.relative_to(source_path)
        if ".git" in relative.parts:
            continue
        if (
            len(relative.parts) > 2
            and relative.parts[0] == "arch"
            and relative.parts[1] != arch
        ):
            continue
        kconfig_files.append(path)
    kconfig_files.sort()
    if not (source_path / "Kconfig").is_file():
        raise ValueError(f"Kernel source Kconfig file not found: {source_path / 'Kconfig'}")

    for path in kconfig_files:
        lines = path.read_text(encoding="utf-8").splitlines()
        name = None
        help_property_indent = None
        help_text_indent = None
        help_lines = []
        index = 0

        while index < len(lines):
            line = lines[index]
            stripped = line.strip()
            indent = len(line) - len(line.lstrip(" \t"))

            if help_property_indent is not None:
                if not stripped:
                    help_lines.append("")
                    index += 1
                    continue
                if help_text_indent is None and indent > help_property_indent:
                    help_text_indent = indent
                if help_text_indent is not None and indent >= help_text_indent:
                    help_lines.append(line)
                    index += 1
                    continue

                if help_text_indent is not None:
                    _append_help(definitions, name, help_lines, help_text_indent)
                help_property_indent = None
                help_text_indent = None
                help_lines = []
                continue

            declaration = CONFIG_DECLARATION.match(line)
            if declaration:
                name = declaration.group(1)
                definitions.setdefault(name, {"prompts": [], "help": []})
                index += 1
                continue

            if STRUCTURAL_LINE.match(stripped):
                name = None
                index += 1
                continue

            if name is not None:
                help_match = HELP_PROPERTY.fullmatch(stripped)
                if help_match:
                    help_property_indent = indent
                    index += 1
                    continue

                prompt_match = (
                    PROMPT_PROPERTY.match(stripped) or PROMPT_LINE.match(stripped)
                )
                if prompt_match:
                    prompt = prompt_match.group(1).replace(r'\"', '"').replace(r"\\", "\\")
                    if prompt not in definitions[name]["prompts"]:
                        definitions[name]["prompts"].append(prompt)

            index += 1

        if help_property_indent is not None and help_text_indent is not None:
            _append_help(definitions, name, help_lines, help_text_indent)

    return definitions


def generate_markdown(config_paths, source_path, options, arch):
    config_names = ", ".join(f"`{path.name}`" for path in config_paths)
    assignment_count = sum(len(values) for values in options.values())
    lines = [
        "# Kernel configuration reference",
        "",
        f"Generated from {config_names} using `{source_path.name}` "
        f"Kconfig files (ARCH={arch}).",
        "",
        f"Options documented: {len(options)} "
        f"({assignment_count} config assignments).",
        "",
    ]

    definitions = read_kconfig_definitions(source_path, arch)

    for name, values in sorted(options.items()):
        definition = definitions.get(name)
        if definition is None:
            prompt = ""
            description = "This option is not defined in the supplied kernel source tree."
        else:
            prompt = "; ".join(definition["prompts"])
            description = "\n\n".join(definition["help"])
            if not description:
                description = "No help text is defined for this option in Kconfig."

        lines.extend([f"## CONFIG_{name}", ""])
        for filename, value in values:
            lines.append(f"- **Value in `{filename}`:** `{value}`")
        lines.extend(
            [
                f"- **Prompt:** {prompt or 'No prompt defined.'}",
                "",
                "**Description**",
                "",
                description,
                "",
            ]
        )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Markdown documentation for kernel .config options."
    )
    parser.add_argument(
        "configs",
        nargs="+",
        type=Path,
        help="One or more kernel config files whose options should be documented",
    )
    parser.add_argument(
        "--kernel-source",
        required=True,
        type=Path,
        help="Root of the matching kernel source tree",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write Markdown to this path (default: stdout)",
    )
    parser.add_argument(
        "--arch",
        default="arm64",
        help="Target architecture (default: arm64)",
    )
    args = parser.parse_args()

    config_paths = [path.resolve() for path in args.configs]
    source_path = args.kernel_source.resolve()
    for config_path in config_paths:
        if not config_path.is_file():
            parser.error(f"config file not found: {config_path}")
    if not source_path.is_dir():
        parser.error(f"kernel source directory not found: {source_path}")

    try:
        options = collect_options(config_paths)
        markdown = generate_markdown(config_paths, source_path, options, args.arch)
    except ValueError as error:
        parser.error(str(error))

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(markdown)


if __name__ == "__main__":
    main()

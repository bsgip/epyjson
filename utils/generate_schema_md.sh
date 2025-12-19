#/bin/bash
generate-schema-doc --config template_name=md --config show_toc=false --config expand_references=true --config no_separate_references=true src/epyjson/e-json-schema.json e-json-schema.md

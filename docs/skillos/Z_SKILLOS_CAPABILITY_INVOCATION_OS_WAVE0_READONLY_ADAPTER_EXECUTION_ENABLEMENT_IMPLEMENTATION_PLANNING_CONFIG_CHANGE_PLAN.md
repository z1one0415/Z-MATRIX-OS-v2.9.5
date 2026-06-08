# Impl ✓ CONFIG_CHANGE_PLAN

## Status: IMPLEMENTATION_PLANNING_CONFIG_CHANGE_PLAN_READY
Phase: WAVE0_ENABLEMENT_IMPLEMENTATION_PLANNING | Level 5: BLOCKED

## GitHub Readonly Adapter Config
| 配置项 | 默认值 | 计划值 |
|:--|:--|:--|
| `adapters.wave0.github_readonly.enabled` | False | False(Phase 12) |
| `adapters.wave0.github_readonly.allowed_orgs` | [] | ["z1one0415"] |
| `adapters.wave0.github_readonly.allowed_repos` | [] | ["Z-MATRIX-OS-v2.9.5"] |
| `adapters.wave0.github_readonly.max_file_size_mb` | 1 | 5 |
| `adapters.wave0.github_readonly.rate_limit_rpm` | 10 | 30 |
| `adapters.wave0.github_readonly.cache_ttl_s` | 300 | 600 |
| `adapters.wave0.github_readonly.token_env` | "" | "GITHUB_READONLY_TOKEN" |

## Document Generation Adapter Config
| 配置项 | 默认值 | 计划值 |
|:--|:--|:--|
| `adapters.wave0.doc_gen.enabled` | False | False(Phase 12) |
| `adapters.wave0.doc_gen.output_dir` | "" | "memory/" |
| `adapters.wave0.doc_gen.max_doc_size_kb` | 100 | 500 |
| `adapters.wave0.doc_gen.allowed_formats` | [] | ["md","txt","json"] |
| `adapters.wave0.doc_gen.template_dir` | "" | "skillos/.../adapters/wave0/templates/" |

## Report Reading Adapter Config
| 配置项 | 默认值 | 计划值 |
|:--|:--|:--|
| `adapters.wave0.report_reader.enabled` | False | False(Phase 12) |
| `adapters.wave0.report_reader.allowed_dirs` | [] | ["docs/","memory/","记忆宫殿/"] |
| `adapters.wave0.report_reader.max_file_size_mb` | 5 | 10 |
| `adapters.wave0.report_reader.forbidden_paths` | [] | ["secrets/","keys/",".env","credentials"] |

## Change Impact: 新增 config keys(Cap OS namespace only) | Token env var(Phase 12) | 新增目录引用 | Risk: Low | 缓解: all disabled default

## Boundary: 不修改 config.yaml/json/pyproject.toml | enabled=False | 不影响 Gateway

## Next: CONFIG_CHANGE_PLAN finalized → Plan 层产出

> Cap OS Phase 11 | Config Change Plan | Level 5 BLOCKED
# Impl ✓ FILE_LEVEL_PLAN

## Status: IMPLEMENTATION_PLANNING_FILE_LEVEL_PLAN_READY
Phase: WAVE0_ENABLEMENT_IMPLEMENTATION_PLANNING | Level 5: BLOCKED

## GitHub Readonly Adapter Files (Phase 12)
| 文件 | 操作 | 说明 |
|:--|:--|:--|
| `adapters/wave0/github_readonly/__init__.py` | CREATE | 包初始化 |
| `adapters/wave0/github_readonly/adapter.py` | CREATE | 主 adapter |
| `adapters/wave0/github_readonly/client.py` | CREATE | GitHub REST API wrapper |
| `adapters/wave0/github_readonly/config.py` | CREATE | 专用配置 |
| `adapters/wave0/github_readonly/cache.py` | CREATE | 内存 LRU 缓存 |
| `adapters/wave0/github_readonly/errors.py` | CREATE | Adapter 异常 |
| `adapters/wave0/github_readonly/operations.py` | CREATE | read_file/list_repos/get_commits |
| `adapters/wave0/base.py` | MODIFY | 注册点 |

## Document Generation Adapter Files
| 文件 | 操作 | 说明 |
|:--|:--|:--|
| `adapters/wave0/doc_gen/__init__.py` | CREATE | 包初始化 |
| `adapters/wave0/doc_gen/adapter.py` | CREATE | 主 adapter |
| `adapters/wave0/doc_gen/generator.py` | CREATE | Markdown→PDF 生成器 |
| `adapters/wave0/doc_gen/templates/` | CREATE | Jinja2 模板目录 |
| `adapters/wave0/doc_gen/config.py` | CREATE | 专用配置 |
| `adapters/wave0/doc_gen/operations.py` | CREATE | generate/validate/template_render |

## Report Reading Adapter Files
| 文件 | 操作 | 说明 |
|:--|:--|:--|
| `adapters/wave0/report_reader/__init__.py` | CREATE | 包初始化 |
| `adapters/wave0/report_reader/adapter.py` | CREATE | 主 adapter |
| `adapters/wave0/report_reader/reader.py` | CREATE | 文件解析器 |
| `adapters/wave0/report_reader/config.py` | CREATE | 专用配置 |
| `adapters/wave0/report_reader/operations.py` | CREATE | read_report/parse/analyze |

## Shared/Testing
| 文件 | 操作 |
|:--|:--|
| `adapters/wave0/__init__.py` | MODIFY(注册3 adapter) |
| `adapters/wave0/registry.py` | MODIFY |
| `tests/skillos/.../test_github_readonly.py` | CREATE |
| `tests/skillos/.../test_doc_gen.py` | CREATE |
| `tests/skillos/.../test_report_reader.py` | CREATE |

## NOT Changed: runtime/ | config.py | zmatrix/ | tests/agent/ | docs/(except skillos/)

## Estimates: ~22 新文件 | ~3 修改 | ~2000-3000 行代码 | ~500-800 行测试

> Cap OS Phase 11 | File-Level Plan | Level 5 BLOCKED | Phase 12 实现
# SGT Skills

Bộ sưu tập các Claude Code Skills chuyên biệt được thiết kế để nâng cao hiệu suất phát triển phần mềm.

## Giới thiệu

SGT Skills là một tập hợp các kỹ năng (skills) module hóa cho Claude Code, cung cấp kiến thức chuyên sâu và quy trình làm việc cho nhiều lĩnh vực phát triển phần mềm khác nhau. Mỗi skill được thiết kế để biến Claude từ một trợ lý tổng quát thành một chuyên gia trong từng lĩnh vực cụ thể.

## Cấu trúc dự án

```
.claude/
├── commands/          # Custom commands cho Claude Code
│   └── git/          # Git workflow commands (cm, cp, pr)
└── skills/           # Collection of skills
    ├── code-review/          # Code review best practices
    ├── context-engineering/  # Context optimization cho AI agents
    ├── debugging/            # Systematic debugging frameworks
    ├── docs-seeker/          # Tìm kiếm tài liệu kỹ thuật
    ├── frontend-design/      # Frontend design patterns
    ├── java-best-practices/  # Java development standards
    ├── laravel-best-practices/ # Laravel MVC + Service architecture
    ├── mermaidjs-v11/        # Diagram creation with Mermaid.js
    ├── problem-solving/      # Creative problem-solving techniques
    ├── react-best-practices/ # React/Next.js optimization (Vercel)
    ├── repomix/              # Codebase packaging cho AI analysis
    ├── sequential-thinking/  # Step-by-step reasoning
    ├── shopify/              # Shopify development
    ├── shopify-development/  # Shopify apps, extensions, themes
    ├── skill-creator/        # Guide for creating new skills
    ├── ui-styling/           # UI/UX với shadcn/ui + Tailwind
    ├── web-design-guidelines/ # Web Interface Guidelines compliance
    └── web-testing/          # E2E, unit, integration, load testing
```

## Các kỹ năng có sẵn

### Core Development

| Skill | Mô tả |
|-------|-------|
| **java-best-practices** | Clean code, SOLID, design patterns, Java 8/17/21+, concurrency, testing, Spring |
| **laravel-best-practices** | MVC + Service architecture, thin controllers, fat models, Form Request validation |
| **react-best-practices** | React/Next.js performance optimization từ Vercel Engineering |

### Frontend & Design

| Skill | Mô tả |
|-------|-------|
| **ui-styling** | shadcn/ui components, Tailwind CSS, canvas-based visual designs |
| **frontend-design** | Production-grade frontend interfaces với high design quality |
| **mermaidjs-v11** | Flowcharts, sequence diagrams, class diagrams, state diagrams |

### Testing & Quality

| Skill | Mô tả |
|-------|-------|
| **web-testing** | Playwright, Vitest, k6 - E2E, unit, integration, load testing |
| **code-review** | Code review practices và verification gates |
| **debugging** | Root cause analysis, defense-in-depth, verification protocols |

### Development Tools

| Skill | Mô tả |
|-------|-------|
| **docs-seeker** | Tìm kiếm tài liệu kỹ thuật (llms.txt, GitHub repos via Repomix) |
| **repomix** | Package codebases thành single AI-friendly files |
| **shopify-development** | Shopify apps, extensions, themes (GraphQL, CLI, Polaris UI) |

### Problem Solving

| Skill | Mô tả |
|-------|-------|
| **problem-solving** | Collision-zone thinking, inversion, pattern recognition |
| **sequential-thinking** | Multi-step reasoning với dynamic adjustment |
| **context-engineering** | Context optimization, compression, memory systems |

## Custom Commands

### Git Workflow (`/cm`, `/cp`, `/pr`)

- **`/cm`**: Stage tất cả files và tạo commit
  - Review modified files
  - Tạo commit message theo convention commit rules
  - Stage và commit changes

- **`/cp`**: Stage, commit và push tất cả code trong branch hiện tại

- **`/pr`**: Tạo Pull Request với summary và test plan

## Cài đặt

1. **Clone repository này vào thư mục `.claude/` của dự án:**

```bash
# Nếu dự án chưa có thư mục .claude
git clone https://github.com/your-org/sgt-skills.git .claude
```

Hoặc copy các skills vào `.claude/skills/`:

```bash
cp -r sgt-skills/.claude/skills/* /path/to/your/project/.claude/skills/
```

2. **Copy custom git commands:**

```bash
cp -r sgt-skills/.claude/commands /path/to/your/project/.claude/
```

3. **Cấu hình MCP Servers (optional):**

Copy và chỉnh sửa `.mcp.json.example` thành `.mcp.json`:

```bash
cp .mcp.json.example .mcp.json
# Edit .mcp.json với API keys của bạn
```

## MCP Servers được hỗ trợ

Dự án bao gồm cấu hình mẫu cho các MCP servers:

- **context7** - Upstash Context7 cho library documentation
- **serena** - Semantic coding tools
- **memory** - Model Context Protocol memory server
- **playwright** - Browser automation
- **sequential-thinking** - Step-by-step reasoning
- **shopify-dev-mcp** - Shopify development tools

## Tạo Skill mới

Sử dụng **skill-creator** để tạo skills mới:

```bash
cd .claude/skills/skill-creator/scripts
python init_skill.py <skill-name> --path <output-directory>
```

Xem thêm tại `.claude/skills/skill-creator/SKILL.md`

## Đóng góp

Contributions are welcome! Các skill mới nên:

1. Theo format chuẩn với `SKILL.md` có YAML frontmatter
2. Giữ SKILL.md dưới 200 lines (sử dụng `references/` cho detailed docs)
3. Bao gồm scripts trong `scripts/` với tests
4. Theo progressive disclosure principle

## License

MIT License - xem LICENSE file để biết thêm chi tiết.

## Tài nguyên

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/)
- [Agent Skills Spec](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/)
- [MCP Protocol](https://modelcontextprotocol.io/)

## 问题格式

### index

描述题目序号，类型为 `int`

### description

- `problem`：描述题面，类型为`str`
- `rules`：描述题目所作的限制规则，类型为`list[str]`

### limit

对玩家 `Input` 内容所作的限制，提供以下几种格式：

- `words_count`：`Input` 内容所能达到的最大字符数，类型为 `int`
- `ban_word`：被禁用的字词，类型为 `list[str]`

### validator

判断 `Output` 是否满足条件的函数


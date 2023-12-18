module.exports = {
  // 一行的字符数，如果超过会进行换行，默认为80
  printWidth: 120,
  // tab缩进大小,默认为2
  tabWidth: 2,
  // 行末分号, 默认true
  semi: true,
  // 使用tab缩进还是空格，默认false
  useTabs: false,
  // 使用单引号, 默认false(在jsx中配置无效, 默认都是双引号)
  singleQuote: true,
  // JSX双引号
  jsxSingleQuote: false,
  // 尽可能使用尾随逗号（包括函数参数）,默认none,可选 none|es5|all
  // es5 包括es5中的数组、对象
  // all 包括函数对象等所有可选
  trailingComma: 'all',
  // 在对象文字中打印括号之间的空格。 默认true
  bracketSpacing: true,
  bracketSameLine: false,
  // 箭头函数参数括号 默认avoid 可选 avoid| always
  // avoid 能省略括号的时候就省略 例如x => x
  // always 总是有括号
  arrowParens: 'avoid',
  // 在文件顶部插入一个特殊的 @format 标记，指定文件格式需要被格式化。
  insertPragma: false,
  // 行尾换行格式
  endOfLine: 'auto',
  // html空格敏感度
  htmlWhitespaceSensitivity: 'ignore',
  // vue缩进脚本和样式
  vueIndentScriptAndStyle: false,
  // > 标签放在最后一行的末尾，而不是单独放在下一行 默认false
  jsxBracketSameLine: false,
};

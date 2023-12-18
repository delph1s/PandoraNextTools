module.exports = {
  // 将 ESLint 限制到一个特定的项目, 停止在父级目录查找
  root: true,
  // 提供运行环境，一个环境定义了一组预定义的全局变量
  env: {
    browser: true,
    es2021: true,
    // node: true,
  },
  // 一个配置文件可以被基础配置中的已启用的规则继承
  // 在已有规则上(包括eslint官方和第三方)上的二次配置
  extends: ['airbnb', 'airbnb-typescript', 'airbnb/hooks', 'prettier'],
  // 自定义全局变量
  globals: {
    React: true,
    JSX: true,
    // _: true,
    // $: true,
  },
  // 针对某个文件或者某类文件特殊化处理
  overrides: [],
  // ESLint 默认使用 Espree 作为其解析器，你可以在配置文件中指定一个不同的解析器
  parser: '@typescript-eslint/parser',
  // 配置解析器支持的语法
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: './tsconfig.json',
    warnOnUnsupportedTypeScriptVersion: false,
  },
  //
  settings: {
    'import/resolver': {
      typescript: {
        alwaysTryTypes: true,
      },
    },
  },
  // 插件自己定义了一些规则，提供给用户使用
  // 在配置文件里配置插件时，可以使用 plugins 关键字来存放插件名字的列表。插件名称可以省略 eslint-plugin- 前缀。
  plugins: ['@typescript-eslint', 'unused-imports', 'simple-import-sort', 'prettier'],
  rules: {
    '@typescript-eslint/ban-ts-comment': 'off',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    '@typescript-eslint/no-empty-function': 'warn',
    '@typescript-eslint/no-explicit-any': 'off',
    "@typescript-eslint/no-use-before-define": 'off',
    'arrow-body-style': [
      'error',
      'as-needed',
      {
        requireReturnForObjectLiteral: true,
      },
    ],
    'import/no-extraneous-dependencies': 'off',
    'import/prefer-default-export': 'off',
    'no-console': 'warn',
    'no-unused-vars': 'off',
    'react/display-name': 'off',
    'react/jsx-curly-brace-presence': ['warn', { props: 'never', children: 'never' }],
    'react/jsx-no-useless-fragment': [
      1,
      {
        allowExpressions: true,
      },
    ],
    'react/jsx-props-no-spreading': 'off',
    'react/no-unescaped-entities': 'off',
    'react/no-unstable-nested-components': [
      1,
      {
        allowAsProps: true,
      },
    ],
    'react/require-default-props': [
      'warn',
      {
        forbidDefaultForRequired: false,
        classes: 'defaultProps', // defaultProps | ignore
        functions: 'defaultArguments', // defaultProps | defaultArguments | ignore
      },
    ],

    // #region  //*=========== Unused Import ===========
    '@typescript-eslint/no-unused-vars': 'off',
    'unused-imports/no-unused-imports': 'off',
    'unused-imports/no-unused-vars': [
      'off',
      {
        vars: 'all',
        varsIgnorePattern: '^_',
        args: 'after-used',
        argsIgnorePattern: '^_',
      },
    ],
    // #endregion  //*======== Unused Import ===========

    // #region  //*=========== Sort Import ===========
    'simple-import-sort/exports': 'warn',
    'simple-import-sort/imports': [
      'warn',
      {
        groups: [
          // ext library & side effect imports
          ['^@?\\w', '^\\u0000'],
          // {s}css files
          ['^.+\\.s?css$'],
          // Lib and hooks
          ['^@/lib', '^@/hooks'],
          // static data
          ['^@/data'],
          // components
          ['^@/components'],
          // Other imports
          ['^@/'],
          // relative paths up until 3 level
          [
            '^\\./?$',
            '^\\.(?!/?$)',
            '^\\.\\./?$',
            '^\\.\\.(?!/?$)',
            '^\\.\\./\\.\\./?$',
            '^\\.\\./\\.\\.(?!/?$)',
            '^\\.\\./\\.\\./\\.\\./?$',
            '^\\.\\./\\.\\./\\.\\.(?!/?$)',
          ],
          ['^@/types'],
          // other that did not fit in
          ['^'],
        ],
      },
    ],
    // #endregion  //*======== Sort Import ===========
  },
};

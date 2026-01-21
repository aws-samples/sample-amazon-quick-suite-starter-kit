import stylisticPlugin from '@stylistic/eslint-plugin';
import typescriptPlugin from '@typescript-eslint/eslint-plugin';
import typescriptParser from '@typescript-eslint/parser';
import importPlugin from 'eslint-plugin-import';
import globals from 'globals';
export default [
  {
    ignores: [
      '*.js',
      '!.projenrc.js',
      '*.d.ts',
      'node_modules/',
      '*.generated.ts',
      'coverage',
      'cdk.out/',
      'lambdas/',
      '**/*.d.ts',
      'operator_tools/'
    ],
  },
  {
    files: ['**/*.{ts}'],
    ignores: ['**/*.d.ts'],
    languageOptions: {
      parser: typescriptParser,
      parserOptions: {
        ecmaVersion: 2020,
        sourceType: 'module',
        project: './tsconfig.json',
      },
      globals: {
        ...globals.jest,
        ...globals.node,
      },
    },
    plugins: {
      '@typescript-eslint': typescriptPlugin,
      import: importPlugin,
      '@stylistic': stylisticPlugin,
    },
    settings: {
      'import/parsers': {
        '@typescript-eslint/parser': ['.ts', '.tsx'],
      },
      'import/resolver': {
        node: true,
        typescript: {
          project: './tsconfig.json',
          alwaysTryTypes: true,
        },
      },
    },
    rules: {
      indent: 'off',
      '@stylistic/indent': ['error', 2],
      '@stylistic/quotes': ['error', 'single', { avoidEscape: true }],
      '@stylistic/comma-dangle': ['error', 'always-multiline'],
      '@stylistic/comma-spacing': ['error', { before: false, after: true }],
      '@stylistic/no-multi-spaces': ['error', { ignoreEOLComments: false }],
      '@stylistic/array-bracket-spacing': ['error', 'never'],
      '@stylistic/array-bracket-newline': ['error', 'consistent'],
      '@stylistic/object-curly-spacing': ['error', 'always'],
      '@stylistic/object-curly-newline': ['error', { multiline: true, consistent: true }],
      '@stylistic/object-property-newline': ['error', { allowAllPropertiesOnSameLine: true }],
      '@stylistic/keyword-spacing': ['error'],
      '@stylistic/brace-style': ['error', '1tbs', { allowSingleLine: true }],
      '@stylistic/space-before-blocks': ['error'],
      '@stylistic/curly': ['error', 'multi-line', 'consistent'],
      '@stylistic/member-delimiter-style': ['error'],
      '@stylistic/semi': ['error', 'always'],
      '@stylistic/max-len': [
        'error',
        {
          code: 120,
          ignoreUrls: true,
          ignoreStrings: true,
          ignoreTemplateLiterals: true,
          ignoreComments: true,
          ignoreRegExpLiterals: true,
        },
      ],
      '@stylistic/quote-props': ['error', 'consistent-as-needed'],
      '@typescript-eslint/no-require-imports': ['error'],
      'import/no-extraneous-dependencies': [
        'error',
        {
          devDependencies: true,
          optionalDependencies: false,
          peerDependencies: true,
        },
      ],
      'import/no-unresolved': ['error'],
      'import/order': [
        'warn',
        {
          groups: ['builtin', 'external'],
          alphabetize: {
            order: 'asc',
            caseInsensitive: true,
          },
        },
      ],
      'no-duplicate-imports': ['error'],
      'no-shadow': 'off',
      '@typescript-eslint/no-shadow': ['error'],
      '@stylistic/key-spacing': ['error'],
      '@stylistic/no-multiple-empty-lines': ['error'],
      '@typescript-eslint/no-floating-promises': ['error'],
      'no-return-await': 'off',
      '@typescript-eslint/return-await': ['error'],
      '@stylistic/no-trailing-spaces': ['error'],
      'dot-notation': ['error'],
      'no-bitwise': ['error'],
      'prefer-destructuring': ['error', {
        'array': true,
        'object': true
      }, {
        'enforceForRenamedProperties': false
      }],
      '@typescript-eslint/member-ordering': [
        'error',
        {
          default: [
            'public-static-field',
            'public-static-method',
            'protected-static-field',
            'protected-static-method',
            'private-static-field',
            'private-static-method',
            'field',
            'constructor',
            'method',
          ],
        },
      ],
    },
  },
];

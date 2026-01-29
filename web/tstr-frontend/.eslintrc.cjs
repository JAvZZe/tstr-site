module.exports = {
    root: true,
    parser: '@typescript-eslint/parser',
    plugins: ['@typescript-eslint', 'react'],
    extends: [
        'eslint:recommended',
        'plugin:@typescript-eslint/recommended',
        'plugin:react/recommended',
        'plugin:react/jsx-runtime',
        'prettier',
    ],
    env: {
        browser: true,
        node: true,
        es2021: true,
    },
    settings: {
        react: {
            version: 'detect',
        },
    },
    rules: {
        '@typescript-eslint/no-unused-vars': [
            'error',
            {
                argsIgnorePattern: '^_',
                varsIgnorePattern: '^_',
                caughtErrorsIgnorePattern: '^_'
            }
        ],
        '@typescript-eslint/no-explicit-any': 'error',
        'react/prop-types': 'off',
        '@typescript-eslint/no-require-imports': 'error',
    },
    ignorePatterns: ['dist/', 'node_modules/', '.astro/', '.wrangler/'],
};

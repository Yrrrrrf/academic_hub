import { join } from 'path'
import type { Config } from 'tailwindcss'
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';
import { skeleton } from '@skeletonlabs/tw-plugin';
import { some_custom_theme } from './src/some_custom_theme'

export default {
	darkMode: 'class',
	content: ['./src/**/*.{html,js,svelte,ts}', join(require.resolve('@skeletonlabs/skeleton'), '../**/*.{html,js,svelte,ts}')],
	theme: {
		extend: {},
	},
	plugins: [
		forms,
		typography,
		skeleton({
			themes: {
				preset: [
					{
						name: 'skeleton',
						enhancements: true,
					},
					{
						name: 'wintry',
						enhancements: true,
					},
					{
						name: 'rocket',
						enhancements: true,
					},
					{
						name: 'vintage',
						enhancements: true,
					},
					{
						name: 'crimson',
						enhancements: true,
					},
					{
						name: 'hamlindigo',
						enhancements: true,
					},
				],
				custom: [
					some_custom_theme,
				],
			},
		}),
	],
} satisfies Config;

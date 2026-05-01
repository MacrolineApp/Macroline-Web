import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://macroline.app',
  output: 'static',
  build: {
    inlineStylesheets: 'auto',
  },
  compressHTML: true,
});

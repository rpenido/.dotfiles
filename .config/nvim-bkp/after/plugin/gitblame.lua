local gitblame = require('gitblame')
gitblame.setup({
  enabled = false,
  date_format = '%Y-%m-%d %H:%M:%S',
})

vim.keymap.set('n','<leader>gb', gitblame.toggle, {});


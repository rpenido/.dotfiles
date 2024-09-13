local Comment = require('Comment')
Comment.setup()

vim.keymap.set("n","<leader>/", '<Plug>(comment_toggle_linewise_current)');
vim.keymap.set("v","<leader>/", '<Plug>(comment_toggle_linewise_visual)');


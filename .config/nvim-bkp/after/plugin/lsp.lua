if vim.g.vscode == nil then
  local lsp_zero = require('lsp-zero')

  require('mason').setup({})

  require('mason-lspconfig').setup({
    ensure_installed = {
      'tsserver',
      'eslint',
      'lua_ls',
      'rust_analyzer',
      'pyright',
    },
    handlers = {
      lsp_zero.default_setup,
      lua_ls = function()
        local lua_opts = lsp_zero.nvim_lua_ls()
        require('lspconfig').lua_ls.setup(lua_opts)
      end,
    }
  })


  -- lsp.configure('lua_ls', {
  --   cmd = { 'lua-language-server' },
  --   settings = {
  --     Lua = {
  --       diagnostics = {
  --         globals = { 'vim' },
  --       },
  --      },
  --   },
  -- })

  local cmp = require('cmp')
  local cmp_select = {behavior = cmp.SelectBehavior.Select}
  local cmp_mappings = lsp_zero.defaults.cmp_mappings({
    ['<C-p>'] = cmp.mapping.select_prev_item(cmp_select),
    ['<C-n>'] = cmp.mapping.select_next_item(cmp_select),
    ['<C-y>'] = cmp.mapping.confirm({ select = true }),
    ["<C-Space>"] = cmp.mapping.complete(),
  })

  -- disable completion with tab
  -- this helps with copilot setup
  cmp_mappings['<Tab>'] = nil
  cmp_mappings['<S-Tab>'] = nil

  -- lsp_zero.setup_nvim_cmp({
  --   mapping = cmp_mappings
  -- })

  lsp_zero.set_preferences({
      sign_icons = {
          error = 'E',
          warn = 'W',
          hint = 'H',
          info = 'I'
      }
  })

  vim.diagnostic.config({
      virtual_text = true,
  })

  lsp_zero.on_attach(function(client, bufnr)
    local opts = {buffer = bufnr, remap = false}

    -- if client.name == "eslint" then
    --     vim.cmd.LspStop('eslint')
    --     return
    -- end

    vim.keymap.set("n", "gd", vim.lsp.buf.definition, opts)
    vim.keymap.set("n", "K", vim.lsp.buf.hover, opts)
    vim.keymap.set("n", "<leader>vws", vim.lsp.buf.workspace_symbol, opts)
    vim.keymap.set("n", "<leader>vd", vim.diagnostic.open_float, opts)
    vim.keymap.set("n", "[d", vim.diagnostic.goto_next, opts)
    vim.keymap.set("n", "]d", vim.diagnostic.goto_prev, opts)
    vim.keymap.set("n", "<leader>vca", vim.lsp.buf.code_action, opts)
    vim.keymap.set("n", "<leader>vrr", vim.lsp.buf.references, opts)
    vim.keymap.set("n", "<leader>vrn", vim.lsp.buf.rename, opts)
    vim.keymap.set("i", "<C-h>", vim.lsp.buf.signature_help, opts)

    local diagnostics_active = true
    vim.keymap.set('n', '<leader>dt', function()
      diagnostics_active = not diagnostics_active
      if diagnostics_active then
        vim.diagnostic.show()
      else
        vim.diagnostic.hide()
      end
    end)

  end)
  lsp_zero.setup()
end

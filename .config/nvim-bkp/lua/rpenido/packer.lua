  -- This file can be loaded by calling `lua require('plugins')` from your init.vim

-- Only required if you have packer configured as `opt`
vim.cmd.packadd('packer.nvim')

return require('packer').startup(function(use)
  -- Packer can manage itself
  use 'wbthomason/packer.nvim'
  use 'lambdalisue/suda.vim'
  use 'stevearc/oil.vim'

  use {
    'nvim-telescope/telescope.nvim', tag = '0.1.x',
    requires = { { 'nvim-lua/plenary.nvim' } }
  }

  use('rose-pine/neovim')
  use('shaunsingh/nord.nvim')
  use('savq/melange-nvim')
  use('folke/tokyonight.nvim')
  use 'Mofiqul/dracula.nvim'
  use 'romainl/Apprentice'
  use 'bluz71/vim-nightfly-colors'

use({ 'nvim-treesitter/nvim-treesitter', run = ':TSUpdate' })
  use('theprimeagen/harpoon')
  use('mbbill/undotree')
  use('tpope/vim-fugitive')

  use {
    'VonHeikemen/lsp-zero.nvim',
    tag = 'v3.x',
    requires = {
      -- LSP Support
      { 'neovim/nvim-lspconfig' },
      { 'williamboman/mason.nvim' },
      { 'williamboman/mason-lspconfig.nvim' },

      -- Autocompletion
      { 'hrsh7th/nvim-cmp' },
      { 'hrsh7th/cmp-buffer' },
      { 'hrsh7th/cmp-path' },
      { 'saadparwaiz1/cmp_luasnip' },
      { 'hrsh7th/cmp-nvim-lsp' },
      { 'hrsh7th/cmp-nvim-lua' },
      { 'hrsh7th/cmp-copilot' },

      -- Snippets
      { 'L3MON4D3/LuaSnip' },
      { 'rafamadriz/friendly-snippets' },

    }
  }

  use('prettier/vim-prettier')

  use('folke/zen-mode.nvim')
  use('github/copilot.vim')

  use('mfussenegger/nvim-dap')

  use({
    'folke/trouble.nvim',
    requires = 'nvim-tree/nvim-web-devicons',
  })

  use({
    'kdheepak/lazygit.nvim',
    requires = 'nvim-lua/plenary.nvim',
  })

  use('numToStr/Comment.nvim')

  use('f-person/git-blame.nvim')


end)

-- require('nordpine').setup({
--    disable_background = true
--})

function ColorMyPencils(color)
	-- color = color or "rose-pine"
	-- color = color or "nord"
	color = color or "tokyonight-storm"
	-- color = color or "dracula"
	-- color = color or "apprentice"
	-- color = color or "nightfly"

	vim.cmd.colorscheme(color)
  vim.api.nvim_set_hl(0, "Normal", { bg = "none" })
	vim.api.nvim_set_hl(0, "NormalFloat", { bg = "none" })
	vim.api.nvim_set_hl(0, "LineNr", { bg = "none" })
	vim.api.nvim_set_hl(0, "SignColumn", { bg = "none" })

end

if vim.g.vscode == nil then
  vim.opt.termguicolors = true
  ColorMyPencils()
end

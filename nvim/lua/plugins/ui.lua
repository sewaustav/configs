-- lua/plugins/ui.lua
return {
  -- 1. Сама строка состояния
  {
    "nvim-lualine/lualine.nvim",
    config = function()
      require("lualine").setup()
    end,
  },
  -- 2. Индикатор работы LSP (показывает, когда сервер грузится)
  {
    "j-hui/fidget.nvim",
    tag = "v1.4.0", -- Рекомендуется зафиксировать версию
    config = function()
      require("fidget").setup({})
    end,
  },
}
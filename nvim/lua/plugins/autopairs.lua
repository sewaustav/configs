-- lua/plugins/autopairs.lua
return {
  "windwp/nvim-autopairs",
  event = "InsertEnter", -- загружать только при начале ввода
  config = function()
    local npairs = require("nvim-autopairs")
    npairs.setup({
      check_ts = true, -- использовать Treesitter для проверки контекста
    })

    -- Интеграция с nvim-cmp (чтобы работало с подсказками)
    local cmp_autopairs = require("nvim-autopairs.completion.cmp")
    local cmp = require("cmp")
    cmp.event:on("confirm_done", cmp_autopairs.on_confirm_done())
  end,
}
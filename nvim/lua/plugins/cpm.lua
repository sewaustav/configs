return {
  "hrsh7th/nvim-cmp",
  dependencies = {
    "hrsh7th/cmp-nvim-lsp",
    "hrsh7th/cmp-buffer",
    "hrsh7th/cmp-path",
    "L3MON4D3/LuaSnip",
    "saadparwaiz1/cmp_luasnip",
  },
  config = function()
      -- Теперь вместо require('lspconfig') используем нативный API Neovim 0.11
      local capabilities = require('cmp_nvim_lsp').default_capabilities()
      local servers = { "gopls", "pyright", "ts_ls", "pasls", "dartls" }
  
      for _, lsp in ipairs(servers) do
          -- НОВЫЙ СИНТАКСИС:
          vim.lsp.config(lsp, {
              install = true, -- автоматически ставить через mason, если нужно
              capabilities = capabilities,
          })
          -- Активируем сервер
          vim.lsp.enable(lsp)
      end
  
      -- Твой автокоманд LspAttach остается без изменений, он правильный
      vim.api.nvim_create_autocmd("LspAttach", {
        callback = function(args)
          local opts = { buffer = args.buf }
          vim.keymap.set("n", "gd", vim.lsp.buf.definition, opts)
          vim.keymap.set("n", "K", vim.lsp.buf.hover, opts)
          vim.keymap.set("n", "<leader>rn", vim.lsp.buf.rename, opts)
          vim.keymap.set("n", "gr", vim.lsp.buf.references, opts)
          vim.keymap.set("n", "<leader>ca", vim.lsp.buf.code_action, opts)
        end,
      })
  end,
}
-- ~/.config/nvim/lua/plugins/lsp.lua
return {
  "neovim/nvim-lspconfig",
  dependencies = {
    { "williamboman/mason.nvim", config = true },
    { "williamboman/mason-lspconfig.nvim", config = true },
    "hrsh7th/cmp-nvim-lsp",
  },
  config = function()
    local status_ok, lspconfig = pcall(require, "lspconfig")
    if not status_ok then
      vim.notify("LSPConfig не загрузился!", vim.log.levels.ERROR)
      return
    end

    local capabilities = require('cmp_nvim_lsp').default_capabilities()
    local servers = { "gopls", "pyright", "ts_ls", "pasls", "dartls" }

    for _, lsp in ipairs(servers) do
      lspconfig[lsp].setup({
        capabilities = capabilities,
      })
    end

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
return {
  "neovim/nvim-lspconfig",
  dependencies = {
    { "williamboman/mason.nvim", config = true },
    "williamboman/mason-lspconfig.nvim", -- Этот парень свяжет Mason и LSP
    "hrsh7th/cmp-nvim-lsp",
  },
  config = function()
    local capabilities = require('cmp_nvim_lsp').default_capabilities()
    
    -- Настраиваем mason-lspconfig, чтобы он сам пинал серверы
    require("mason-lspconfig").setup({
      ensure_installed = { "pyright", "gopls", "ts_ls" }, -- Он сам их поставит!
    })

    -- Новый способ инициализации для Neovim 0.11+
    -- Если vim.lsp.config существует, используем его, иначе старый метод
    local servers = { "gopls", "pyright", "ts_ls", "pasls", "dartls" }

    for _, lsp in ipairs(servers) do
      if vim.lsp.config then
        -- Синтаксис 0.11
        vim.lsp.config(lsp, { capabilities = capabilities })
        vim.lsp.enable(lsp)
      else
        -- Старый добрый синтаксис (на случай откатки версии)
        require('lspconfig')[lsp].setup({ capabilities = capabilities })
      end
    end

    -- Твои бинды остаются тут же
    vim.api.nvim_create_autocmd("LspAttach", {
      callback = function(args)
        local opts = { buffer = args.buf }
        vim.keymap.set("n", "gd", vim.lsp.buf.definition, opts)
        vim.keymap.set("n", "K", vim.lsp.buf.hover, opts)
      end,
    })
  end,
}
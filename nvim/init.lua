local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable",
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
  {
    "nvim-tree/nvim-tree.lua",
    version = "*",
    lazy = false,
    dependencies = {
      "nvim-tree/nvim-web-devicons", -- File icons
    },
    config = function()
      require("nvim-tree").setup({
        view = {
          width = 30,
          side = "left",
          number = true, -- Enable line numbers in nvim-tree
          relativenumber = true, -- Enable relative line numbers
        },
        renderer = {
          icons = {
            show = {
              file = true,
              folder = true,
              folder_arrow = true,
              git = true,
            },
          },
        },
        filters = {
          dotfiles = false,
          git_ignored = false,
        },
        actions = {
          open_file = {
            quit_on_open = false,
            window_picker = {
              enable = true, -- Включаем выбор окна для сплитов
            },
          },
        },
      })
      vim.keymap.set("n", "<C-n>", ":NvimTreeToggle<CR>", { desc = "Toggle nvim-tree" })
      vim.keymap.set("n", "<leader>e", ":NvimTreeFocus<CR>", { desc = "Focus nvim-tree" })
      vim.keymap.set("n", "<C-v>", ":NvimTreeOpen vsplit<CR>", { desc = "Open file in vertical split" })
      vim.keymap.set("n", "<C-x>", ":NvimTreeOpen split<CR>", { desc = "Open file in horizontal split" })
    end,
  },
  {
    "neoclide/coc.nvim",
    branch = "release",
    config = function()
      -- Расширения coc.nvim
      vim.g.coc_global_extensions = { 'coc-go', 'coc-json', 'coc-yaml', 'coc-pyright' }

      -- Подтверждение автодополнения на <CR>
      vim.keymap.set("i", "<CR>",
        [[coc#pum#visible() ? coc#pum#confirm() : "\<CR>"]],
        { expr = true, silent = true }
      )

      -- Навигация по LSP
      vim.keymap.set("n", "gd", "<Plug>(coc-definition)", { silent = true })
      vim.keymap.set("n", "gy", "<Plug>(coc-type-definition)", { silent = true })
      vim.keymap.set("n", "gi", "<Plug>(coc-implementation)", { silent = true })
      vim.keymap.set("n", "gr", "<Plug>(coc-references)", { silent = true })

      -- Диагностика
      vim.keymap.set("n", "<leader>cd", "<Plug>(coc-diagnostic-prev)", { silent = true, desc = "Previous diagnostic" })
      vim.keymap.set("n", "<leader>cn", "<Plug>(coc-diagnostic-next)", { silent = true, desc = "Next diagnostic" })

      -- Документация
      vim.keymap.set("n", "K", function()
        if vim.fn.index({ "vim", "help" }, vim.bo.filetype) >= 0 then
          vim.cmd("h " .. vim.fn.expand("<cword>"))
        else
          vim.fn.CocAction("doHover")
        end
      end, { silent = true })

      -- Быстрый фикс
      vim.keymap.set("n", "<leader>qf", "<Plug>(coc-fix-current)", { silent = true, desc = "Quickfix current diagnostic" })
    end,
  },
  {
    "windwp/nvim-autopairs",
    config = function()
      local npairs = require("nvim-autopairs")
      npairs.setup({
        disable_filetype = { "TelescopePrompt", "vim" },
        enable_check_bracket_line = true,
        fast_wrap = {},
        check_ts = true,
        map_cr = false, -- отключаем встроенный Enter у autopairs
      })

      -- Подружить autopairs + coc.nvim
      vim.keymap.set("i", "<CR>", function()
        if vim.fn["coc#pum#visible"]() == 1 then
          return vim.fn["coc#pum#confirm"]()
        else
          return npairs.autopairs_cr()
        end
      end, { expr = true, silent = true })
    end,
  },
  {
    "ray-x/go.nvim",
    dependencies = { "ray-x/guihua.lua" },
    config = function()
      require("go").setup({
        gofmt = "gopls", -- Format using gopls
        lsp_cfg = true, -- Use gopls without custom capabilities
        lsp_gofumpt = true, -- Strict gofmt
        dap_debug = true, -- Debugging support
        diagnostic = {
          hdlr = false, -- Let coc.nvim handle diagnostics
        },
      })
      -- Auto-format Go files on save
      vim.api.nvim_create_autocmd("BufWritePre", {
        pattern = "*.go",
        callback = function()
          require("go.format").gofmt()
        end,
      })
    end,
    ft = { "go", "gomod" },
    build = ':lua require("go.install").update_all_sync()',
  },
  {
    "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
    config = function()
      require("nvim-treesitter.configs").setup({
        ensure_installed = { "go", "lua", "python", "bash", "json", "yaml" },
        highlight = { enable = true },
        indent = { enable = true },
      })
    end,
  },
  {
    "loctvl842/monokai-pro.nvim",
    config = function()
      require("monokai-pro").setup({
        filter = "pro",
      })
      vim.cmd("colorscheme monokai-pro")
    end,
  },
})

-- General Neovim settings
vim.opt.number = true -- Enable line numbers
vim.opt.relativenumber = true -- Enable relative line numbers
vim.opt.tabstop = 4 -- 4 spaces for tabs
vim.opt.shiftwidth = 4 -- 4 spaces for indentation
vim.opt.expandtab = true -- Use spaces instead of tabs
vim.opt.smartindent = true -- Smart indentation
vim.opt.termguicolors = true -- Enable true colors
vim.opt.clipboard = "unnamedplus" -- Enable system clipboard

-- System clipboard keymaps for visual mode
vim.keymap.set("v", '"+y', '"+y', { desc = "Yank to system clipboard" })
vim.keymap.set("v", '"+p', '"+p', { desc = "Paste from system clipboard" })

-- Function for coc.nvim completion
function _G.check_back_space()
  local col = vim.fn.col(".") - 1
  return col == 0 or vim.fn.getline("."):sub(col, col):match("%s") ~= nil
end

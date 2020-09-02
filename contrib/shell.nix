let

  # pkgs = import ./nixpkgs.nix {
  pkgs = import <nixpkgs> {
    overlays = [
      # latest version of poetry and poetry2nix
      (import "${poetry2nixSrc}/overlay.nix")
    ];
  };

  # temporary overlay (remove on next nixpkgs bump)
  poetry2nixSrc = (fetchTarball {
    url = "https://github.com/teto/poetry2nix/archive/44f5092c6373ebb0a53bd0e3828ebdb58ab1612b.tar.gz";
    sha256 = "09728x7snn6z8qaqqirs2gc9g8rxrvamiw37qhwp1yvmp9q5b771";
  });

  mptcpanalyzer = pkgs.callPackage ../default.nix {};

  prog = (mptcpanalyzer.override({
    # inherit pandas;
    # inherit cmd2;
  })).overridePythonAttrs (oa: {


    version = "0.3.3-dev";
    nativeBuildInputs = (oa.nativeBuildInputs or []) ++ [
      # to publish on pypi
      # pkgs.python3Packages.twine
      # pkgs.python-language-server

    ];
    propagatedBuildInputs  = (oa.propagatedBuildInputs  or []) ++ [
      # my_nvim.config.python3Env

      # temporary addition to work with mpls
      # pks.openssl
    ];

    src = ../.;

    # postShellHook = ''
    # export PATH="${my_nvim}/bin:$PATH"
    #   echo "importing a custom nvim ${my_nvim}"
    postShellHook = ''
      export SOURCE_DATE_EPOCH=315532800
      echo "SOURCE_DATE_EPOCH: $SOURCE_DATE_EPOCH"
      export PYTHONPATH="$tmp_path/lib/python3.7/site-packages:$PYTHONPATH"
      python -m pip install -e . --prefix $tmp_path >&2

      alias m=mptcpanalyzer
    '';

  });


  # https://www.reddit.com/r/neovim/comments/b1zm7h/how_to_setup_microsofts_python_lsp_in_linuxubuntu/
  # my_nvim = genNeovim  [ mptcpanalyzer ] {
    # plugins = [ vimPlugins.coc-python ];
    # configure = {
    #     packages.myVimPackage = {
    #       # see examples below how to use custom packages
    #       # loaded on launch
    #       start = startPlugins;
    # };
    # configure.packages.myVimPackage.start = [];
    # # extraPython3Packages = ps: with ps;  [ python-language-server ];
  # };

  # prog2 = pkgs.poetry2nix.mkPoetryEnv {
  prog2 = pkgs.poetry2nix.mkPoetryApplication {
    # because shell.nix is in contrib/ folder
    projectDir = ../.;
    # editablePackageSources = {
    #   mptcpanalyzer = ./.;
    # };
  };
in
# TODO generate our own nvim
  prog2

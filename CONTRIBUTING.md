# Set up dev environment

1. Install [nix](https://nixos.org/download.html)

2. Fork and clone the repository

```sh
gh repo fork --clone --remote ibis-project/ibis-substrait
```

3. Set up public `ibis-substrait` Cachix cache to pull pre-built dependencies:

```sh
nix-shell -p cachix --run 'cachix use ibis-substrait'
```

4. Run `nix-shell` in the checkout directory

```sh
cd ibis-substrait
nix-shell
```

### Building the library

```sh
nix develop '.#release' --extra-experimental-features nix-command --extra-experimental-features flakes -c poetry build
```


# Writing commit messages

`ibis-substrait` follows the [Conventional
Commits](https://www.conventionalcommits.org/) structure.  In brief, the commit
summary should look like:

    fix(types): make all floats doubles

The type (e.g. `fix`) can be:

- `fix`: A bug fix. Correlates with PATCH in SemVer
- `feat`: A new feature. Correlates with MINOR in SemVer
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)

  If the commit fixes a Github issue, add something like this to the bottom of the description:

      fixes #4242

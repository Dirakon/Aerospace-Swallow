<h1 align="center">
  Swallow
</h1>
<h4 align="center">Used to swallow (send to the scratchpad) a terminal window after a blocking application is run in Aerospace window manager</h4>

## Information

## Requirements

- MacOS system with Aerospace installed (in a way that `aerospace` binary is in PATH)
- Python3.x+ or nix

## Installation Instruction

### Nix

On systems with nix, you can just use the current repo as a flake input.

I.e.

```nix
# flake.nix
inputs.aerospace-swallow.url = "github:Dirakon/Aerospace-Swallow";
```

and

```nix
# flake.nix
outputs = inputs:
{
    # aerospace-swallow program is now under inputs.aerospace-swallow.default."aarch64-darwin"
    # install it in whatever way suits you
    # ...
}
```

(or use overlays)

### Non-nix

You would need python (as per flake.nix and flake.lock - tested only on python 3.12.5).

Just do 

```bash
python main.py *ANY COMMAND*
```

## Usage

```bash
aerospace-swallow *ANY COMMAND*
```

For example, run Neovide and hide the current terminal app while Neovide is active
```bash
aerospace-swallow neovide --no-fork .
```

## Warning

As per current simplistic implementation, the "hiding" window just goes to a workspace named "scratchpad". If something goes wrong, you can manually visit that workspace - `aerospace workspace scratchpad`

## License

This Project is licensed under the MIT License. Check license file for more info.

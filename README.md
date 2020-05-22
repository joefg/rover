# rover
## a plugin manager for ranger

## Installation
### Dependencies
* `ranger`;
* `git`.

### Setup
Clone this repository into your `ranger` plugins directory, then run the makefile.

Simply:

```
git clone https://github.com/joefg/rover.git
cd rover
make
```

If you don't have `make`, you can just symlink the file over into the plugins directory:

```
git clone https://github.com/joefg/rover.git
ln -s rover/rover.py rover.py
```

## Usage
### Starting
To get started, you'll need a `plugins.json` manifest, in your plugins directory. An example looks like this:

```
[
	"https://github.com/joefg/rover",
	"https://github.com/maximtrp/ranger-archives"
]
```

There is a command to go straight to this manifest in the plugin: `rover_plugins`.

### Installing Plugins
To install your plugins, simply run `:rover_update` inside `ranger`.

For this to work, your plugin needs to be distributed as a `git` repository. A good example of this is [ranger-archives](https://github.com/maximtrp/ranger-archives).

This is because this script uses `git` to clone these repositories (along with fetching from upstream).

### Cleaning Plugins
To purge unused plugins, simply run `:rover_clean` inside `ranger`.

This works by seeing which repositories in the plugins directory don't correspond to repositories listed in `plugins.json`. If there's a directory there that isn't in `plugins.json`, it gets removed.

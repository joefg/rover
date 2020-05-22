# rover
## a plugin manager for ranger

## Installation
Clone this repository into your `ranger` plugins directory, then run the makefile.

Simply:

```
git clone https://github.com/joefg/rover.git
cd rover
make
```

If you don't have `make`, you can just copy the `rover.py` file over into the plugins directory:

```
git clone https://github.com/joefg/rover.git
cp rover/rover.py rover.py
```

## Usage
### Starting
To get started, you'll need a `plugins.json` manifest, in your plugins directory. An example looks like this:

[
    "https://github.com/joefg/rover"
	"https://github.com/maximtrp/ranger-archives"
]

There is a command to go straight to this manifest in the plugin: `rover_plugins`.

# SBOL Visual CSS

SBOL Visual CSS (see [full documentation online](http://edinburgh-genome-foundry.github.io/SBOL-Visual-CSS/) or in [docs/index.html](docs/index.html))
is a pure-CSS library to easily display schematic DNA sequences in the Visual SBOL standard using a simple HTML syntax:

```
<div class="sbol-visual centered">
    <div class="sbolv promoter">p1</div>
    <div class="sbolv cds">lac</div>
    <div class="sbolv terminator">terminator</div>
</div>
```

While very light, SBOL Visual CSS is has features such as inline SBOL and
combinatorial assemblies, and is versatile enough to serve
as a generic SBOL visualizer for databases, web articles, etc.
It is distributed as a self-contained CSS file generated in [dist/sbol-visual-standalone.css](dist/sbol-visual-standalone.css) and
is therefore fit for embedding into HTML emails.

## Build

The project now uses one central Python script:

```bash
python source/build.py
```

This command will:

- compile all SVG icons from `source/SVG/` into `source/icons.json`
- generate the standalone stylesheet `source/sbol-visual.css`
- publish the standalone bundle into `dist/`
- publish the website assets into `docs/dist/`
- sync the example files into `docs/examples/`


SBOL-visual CSS was originally written at the [Edinburgh Genome Foundry](http://genomefoundry.org/) by [Zulko](https://github.com/Zulko).
The code is released on [Github](https://github.com/Edinburgh-Genome-Foundry/SBOL-Visual-CSS) under the MIT License (Copyright Edinburgh Genome Foundry), everyone is welcome to contribute.

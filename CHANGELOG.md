# textX-dev changelog

All _notable_ changes to this project will be documented in this file.

The format is based on _[Keep a Changelog][keepachangelog]_, and this project
adheres to _[Semantic Versioning][semver]_.

Everything that is documented in the [official docs][textXDocs] is considered
the part of the public API.

Backward incompatible changes are marked with **(BIC)**. These changes are the
reason for the major version increase so when upgrading between major versions
please take a look at related PRs and issues and see if the change affects you.

## [Unreleased]


## [0.2.0] (Released: 2025-05-07)

### Changed
- moved to pyproject.toml
- removed : from questions


## [0.1.6] (Released: 2025-04-11)

### Added
- generate tests folder
- generate GitHub Actions config
- config for file extensions if project type is generator


### Fixed
- getting model file name


## [0.1.5] (Released: 2020-10-05)

### Fixed

- Fix setup to package grammar (*.tx) files
  ([5f09f67](https://github.com/textx/textX-dev/commit/5f09f67))


## [0.1.4] (Released: 2020-08-05)

- Added `project_name` to `config`


## [0.1.3] (Released: 2020-08-05)

- Fixed wheel packaging of template files


## [0.1.2] (Released: 2020-08-03)

- Initial release


[Unreleased]: https://github.com/textX/textX-dev/compare/0.2.0...HEAD
[0.2.0]: https://github.com/textX/textX-dev/compare/0.1.6...0.2.0
[0.1.6]: https://github.com/textX/textX-dev/compare/0.1.5...0.1.6
[0.1.5]: https://github.com/textX/textX-dev/compare/0.1.4...0.1.5
[0.1.4]: https://github.com/textX/textX-dev/compare/0.1.3...0.1.4
[0.1.3]: https://github.com/textX/textX-dev/compare/0.1.2...0.1.3
[0.1.2]: https://github.com/textX/textX-dev/tree/0.1.2


[keepachangelog]: https://keepachangelog.com/
[semver]: https://semver.org/spec/v2.0.0.html
[textXDocs]: http://textx.github.io/textX/latest/

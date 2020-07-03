# Handbell Manager for Mac Developer Notes

## Release Checklist

1. Update the version number in the code
  1. It's the VERSION variable at the top of `HandbellManagerMac.py`
2. Create a commit for the release. E.g. `git commit -a -m 'version 1.0.0'`
3. Tag the release. E.g. `git tag v1.0.0`
4. Push the tagged release commit to GitHub
  1. `git push; git push --tags`
5. Open development on the next release
  1. Update the version number in the code to the next version (e.g. `1.1.0-SNAPSHOT`)
6. Create the release on the GitHub [Releases page](https://github.com/SimonGay/HandbellManagerMac/releases/)
7. Put in a PR to update the Homebrew formula in the [`bellringers/bellringing` tap](https://github.com/bellringers/homebrew-bellringing).

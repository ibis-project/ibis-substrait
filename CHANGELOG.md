Release Notes
---

## [4.0.0](https://github.com/ibis-project/ibis-substrait/compare/v3.2.1...v4.0.0) (2024-07-03)

### ⚠ BREAKING CHANGES

* ibis-substrait no longer supports versions of Ibis <
9.x. If you are using an older version of Ibis, you can pin `ibis-substrait<4`

Co-authored-by: Gil Forsyth <gil@forsyth.dev>
Co-authored-by: Gil Forsyth <gforsyth@users.noreply.github.com>

### Features

* add support for Ibis 9.x ([#1034](https://github.com/ibis-project/ibis-substrait/issues/1034)) ([390905e](https://github.com/ibis-project/ibis-substrait/commit/390905e464d29896bf0a4753a71136c1e0335f99))

### Documentation

* remove defunct proto instructions, add commit guide ([c5fcb97](https://github.com/ibis-project/ibis-substrait/commit/c5fcb9713d4d80908c4dc08d4fb67d4bb5986a28))

## [3.2.1](https://github.com/ibis-project/ibis-substrait/compare/v3.2.0...v3.2.1) (2024-05-21)


### Bug Fixes

* **deps:** pin ibis-framework to less than 9 ([f671438](https://github.com/ibis-project/ibis-substrait/commit/f6714386f961a0b987b79358e339b78e352044eb))

## [3.2.0](https://github.com/ibis-project/ibis-substrait/compare/v3.1.1...v3.2.0) (2024-02-06)


### Features

* **autocast:** add autocast for digits argument to ops.Round ([f0d4940](https://github.com/ibis-project/ibis-substrait/commit/f0d49403fd2185571b5e170919ce04ebd0bea4d7))
* support ibis 7.2 ([5976b9f](https://github.com/ibis-project/ibis-substrait/commit/5976b9f15e7eea8187ec4dbf70535029472fffb8))


### Bug Fixes

* **deps:** update dependency ibis-framework to v7.1.0 [security] ([bdb5906](https://github.com/ibis-project/ibis-substrait/commit/bdb590613266321c24369b84f31c4c1e8ba68533))
* **deps:** update dependency packaging to v23.2 ([82d9a9b](https://github.com/ibis-project/ibis-substrait/commit/82d9a9b13fdf30c80b5c0a66c6fae358b07b80dd))
* **grouping:** collect multiple grouping keys in single "groupings" ([30d35e3](https://github.com/ibis-project/ibis-substrait/commit/30d35e3c47baf2e4ddd2811940bae7524c8a37a8))

## [3.1.1](https://github.com/ibis-project/ibis-substrait/compare/v3.1.0...v3.1.1) (2023-10-05)


### Bug Fixes

* **extensions:** pass over extension top-matter ([c7f3e34](https://github.com/ibis-project/ibis-substrait/commit/c7f3e34b7741b3f8541b7c1fb837db5eeadbbe47))
* **extensions:** use compound signature when creating new URI ([d0ee145](https://github.com/ibis-project/ibis-substrait/commit/d0ee1457c095a29af1632f637060c22671f1f501))

## [3.1.0](https://github.com/ibis-project/ibis-substrait/compare/v3.0.0...v3.1.0) (2023-08-30)


### Features

* add type signature to scalar function name definitions ([fe19d3c](https://github.com/ibis-project/ibis-substrait/commit/fe19d3caa0447e5669323cfd74fc7621a1b9ec6b))


### Bug Fixes

* **deps:** update dependency ibis-framework to v6.1.0 ([721d574](https://github.com/ibis-project/ibis-substrait/commit/721d574f05ed43910f231b917a7586e10ef43a27))

## [3.0.0](https://github.com/ibis-project/ibis-substrait/compare/v2.29.1...v3.0.0) (2023-08-02)


### ⚠ BREAKING CHANGES

* The minimum supported version of Ibis is 4.0.
Deprecated methods `sort_by` and `groupby` have been removed in Ibis
6.x, so it is not possible to support 3.x through 6.x.
* **decompile:** decompiler is no longer supported and has been removed.
* **substrait-python:** We now rely on the upstream `substrait`
package (https://github.com/substrait-io/substrait-python) for the
generated substrait code. You will need to install `substrait` from pypi
or conda-forge if you have not already done so.

All tests are passing -- this also accompanies a bump of the Substrait
version to v0.30.0 (because this is what is available in the upstream).

### Features

* add support for Ibis 6.x ([fcfc595](https://github.com/ibis-project/ibis-substrait/commit/fcfc595ca20ff49b41fd100a44a848d63a256f1e))
* **substrait-python:** use upstream substrait python package ([4b38bae](https://github.com/ibis-project/ibis-substrait/commit/4b38bae5ff8f58ac9fcddeb306ed252f5bfbeb3b))


### Bug Fixes

* **deps:** update dependency pyyaml to v6.0.1 ([77f8b40](https://github.com/ibis-project/ibis-substrait/commit/77f8b40f4e8deef40a552c06cc975586f0f5e9af))
* **release:** use `@google/semantic-release-replace-plugin@1.2.0` to avoid module loading bug ([5c6f4fa](https://github.com/ibis-project/ibis-substrait/commit/5c6f4fa40009e7dccf54a49a379c67dc600f40a8))


### Refactors

* **decompile:** remove decompiler ([401bb60](https://github.com/ibis-project/ibis-substrait/commit/401bb607847fa240a50adfbfd7d76a8347e04efc))
* drop support for Ibis 3.x ([9ffaf99](https://github.com/ibis-project/ibis-substrait/commit/9ffaf994fd9b20a46279ad4c23cea1b2ce264155))
* drop support for Python 3.8 ([023351b](https://github.com/ibis-project/ibis-substrait/commit/023351b2c8fcd4848cc4f6fa6515e5761f519b49))
* remove deprecated importlib.resources.path call ([e20542b](https://github.com/ibis-project/ibis-substrait/commit/e20542b1583783620bdf56a8d959061990bb7d7c))

## [2.29.1](https://github.com/ibis-project/ibis-substrait/compare/v2.29.0...v2.29.1) (2023-06-30)


### Bug Fixes

* **deps:** update dependency packaging to v23.1 ([82d38a5](https://github.com/ibis-project/ibis-substrait/commit/82d38a53ed6dc58c0f854d57c281ed5ca816341f))


### Documentation

* add documentation to test_pyarrow::test_extension_udf ([d024b08](https://github.com/ibis-project/ibis-substrait/commit/d024b082078d08060d4c349844e640429cc0450a))


### Refactors

* uses clearer import name for pyarrow.substrait ([65ba567](https://github.com/ibis-project/ibis-substrait/commit/65ba567e1200d7951ae6f6849b1e0b6eefa34889))

## [2.29.0](https://github.com/ibis-project/ibis-substrait/compare/v2.28.2...v2.29.0) (2023-05-17)


### Features

* add support for ibis 5.x ([22c56b6](https://github.com/ibis-project/ibis-substrait/commit/22c56b604d5e96c4a3eae060f5c82d1f1afe0ab3))

## [2.28.2](https://github.com/ibis-project/ibis-substrait/compare/v2.28.1...v2.28.2) (2023-05-17)


### Bug Fixes

* **uri:** allow overriding extension uri when registering extension file ([59d5b29](https://github.com/ibis-project/ibis-substrait/commit/59d5b29944e60f8dc1939d130b0e33996568a1fc))


### Refactors

* change compiler to required keyword arg ([15737f3](https://github.com/ibis-project/ibis-substrait/commit/15737f3a8a0323cb6c4296ba725f4f7e274bf32e))
* **deps:** loosen user-facing protobuf dependency ([88723a1](https://github.com/ibis-project/ibis-substrait/commit/88723a19b82a91ef04e3c148f9329ec4458b4ecc))
* remove expr arguments in translate ([99649dc](https://github.com/ibis-project/ibis-substrait/commit/99649dc2d71ee801b984965610ad3e44cf47475e))

## [2.28.1](https://github.com/ibis-project/ibis-substrait/compare/v2.28.0...v2.28.1) (2023-04-19)


### Bug Fixes

* **window functions:** handle window function ranges correctly ([1352183](https://github.com/ibis-project/ibis-substrait/commit/1352183598234ea27f11f47d95bd67342806207c))

## [2.28.0](https://github.com/ibis-project/ibis-substrait/compare/v2.27.0...v2.28.0) (2023-04-19)


### Features

* add support for std_dev and variance ([#583](https://github.com/ibis-project/ibis-substrait/issues/583)) ([e6cfb6c](https://github.com/ibis-project/ibis-substrait/commit/e6cfb6cf5c87e1ce1dc31e8a280a963e46b11870))

## [2.27.0](https://github.com/ibis-project/ibis-substrait/compare/v2.26.1...v2.27.0) (2023-04-18)


### Features

* **version:** add version to produced substrait plans ([7f83f52](https://github.com/ibis-project/ibis-substrait/commit/7f83f525991b68b023a41cd2e3d986c50b1183eb))

## [2.26.1](https://github.com/ibis-project/ibis-substrait/compare/v2.26.0...v2.26.1) (2023-03-24)


### Bug Fixes

* emit output of projection node to be based off input table instead of source tables ([c0076bc](https://github.com/ibis-project/ibis-substrait/commit/c0076bcf6a1959e4f60308d505bd08ab8d31b103))

## [2.26.0](https://github.com/ibis-project/ibis-substrait/compare/v2.25.1...v2.26.0) (2023-03-14)


### Features

* **udf:** add support for pyarrow / acero UDFs ([9bc455b](https://github.com/ibis-project/ibis-substrait/commit/9bc455bd2a03dcfd34c42ea35d4e4fed50c03c23))


### Bug Fixes

* **cast:** specify failure behavior in cast call ([a5ed55e](https://github.com/ibis-project/ibis-substrait/commit/a5ed55e559cb570b7885aef0b8d8940a6ed54c21))

## [2.25.1](https://github.com/ibis-project/ibis-substrait/compare/v2.25.0...v2.25.1) (2023-03-14)


### Bug Fixes

* **deps:** add pyyaml to runtime dependencies ([59ed976](https://github.com/ibis-project/ibis-substrait/commit/59ed9769e35244f6890df535e4273e0f7d1f6b4a))

## [2.25.0](https://github.com/ibis-project/ibis-substrait/compare/v2.24.1...v2.25.0) (2023-03-14)


### Features

* **extensions:** add correct extension URI to all scalar function calls ([8167cb8](https://github.com/ibis-project/ibis-substrait/commit/8167cb8ea5b796f55afe7d13396a726e062ef325))
* **extensions:** add extension yaml to package ([74ec00f](https://github.com/ibis-project/ibis-substrait/commit/74ec00f6c7499d82826cf8a7cd9b33c82c7dc8a4))

## [2.24.1](https://github.com/ibis-project/ibis-substrait/compare/v2.24.0...v2.24.1) (2023-03-10)


### Bug Fixes

* cast floor and ceil to integer types to workaround acero ([0d52d4d](https://github.com/ibis-project/ibis-substrait/commit/0d52d4d65bdf5094e3c82ed3e1ff3948c16ab53f))

## [2.24.0](https://github.com/ibis-project/ibis-substrait/compare/v2.23.0...v2.24.0) (2023-03-02)


### Features

* **round:** add ops mapping for `round` scalar func ([3f4b5a7](https://github.com/ibis-project/ibis-substrait/commit/3f4b5a7431458c21c2311e62d58b7026cb837143))

## [2.23.0](https://github.com/ibis-project/ibis-substrait/compare/v2.22.0...v2.23.0) (2023-03-02)


### Features

* add substrait mappings for bitwise ops ([92911da](https://github.com/ibis-project/ibis-substrait/commit/92911dae02b98f29dd46f8680c0eaee3aee5789b))

## [2.22.0](https://github.com/ibis-project/ibis-substrait/compare/v2.21.1...v2.22.0) (2023-02-22)


### Features

* **substrait:** bump substrait version to 0.24.0 ([54b1ebd](https://github.com/ibis-project/ibis-substrait/commit/54b1ebdffa5c679c75cbee84a287babcf5acbc01))

## [2.21.1](https://github.com/ibis-project/ibis-substrait/compare/v2.21.0...v2.21.1) (2023-02-08)


### Bug Fixes

* **columns:** remove use of removed (upstream) get_columns ([4d5e991](https://github.com/ibis-project/ibis-substrait/commit/4d5e99146d1b57255029c968367eb1f8cd5843dc))

## [2.21.0](https://github.com/ibis-project/ibis-substrait/compare/v2.20.0...v2.21.0) (2023-02-08)


### Features

* **subquery:** add support for ExistsSubquery and NotExistsSubquery ([f564018](https://github.com/ibis-project/ibis-substrait/commit/f5640189734cec4de5a17f3332997769e2958998))

## [2.20.0](https://github.com/ibis-project/ibis-substrait/compare/v2.19.0...v2.20.0) (2023-02-08)


### Features

* adding substrait mappings for ibis approx ops ([310e3e6](https://github.com/ibis-project/ibis-substrait/commit/310e3e6d47635f4f79a78d3090ae11a4816ddfec))
* **ops:** add rules for ops.TableArrayView and ops.SelfReference ([49a980e](https://github.com/ibis-project/ibis-substrait/commit/49a980e4f3e08eac599ddae93949223a2c8fb025))


### Bug Fixes

* **contains:** allow for isin ops to have a single option ([f0bcbe9](https://github.com/ibis-project/ibis-substrait/commit/f0bcbe93206c5ab7185a3ebd3af9fc203c342f98))
* **emit:** check all rel types for existing output mapping ([51d69a9](https://github.com/ibis-project/ibis-substrait/commit/51d69a9c54581dfabd489978474a69629bbe65ff))
* **ibis-3.x:** add alias for mapping ops.Value -> ops.ValueOp ([ed78bdf](https://github.com/ibis-project/ibis-substrait/commit/ed78bdf3213ebcc53c6325d2a3897afaece1c2e8))
* **substrait:** regenerate proto stubs ([f101aab](https://github.com/ibis-project/ibis-substrait/commit/f101aabdae236fb4860955e37225e69a61815ecc))


### Refactors

* clean up output mapping in ops.Selection dispatch ([d27e8f0](https://github.com/ibis-project/ibis-substrait/commit/d27e8f00aad12d36f4ead30d83df8ebc4b433e55))


### Documentation

* **README:** add simple usage example to README ([b3fa3ac](https://github.com/ibis-project/ibis-substrait/commit/b3fa3acc1e2ccce31ada38e1176ba673a5c9a1b3))

## [2.19.0](https://github.com/ibis-project/ibis-substrait/compare/v2.18.0...v2.19.0) (2023-01-12)


### Features

* add initial support for ibis 4.x ([550b61e](https://github.com/ibis-project/ibis-substrait/commit/550b61e70e8ac45903b01720de37a1fc0b90e083))

## [2.18.0](https://github.com/ibis-project/ibis-substrait/compare/v2.17.0...v2.18.0) (2022-11-16)


### Features

* add more string mappings ([5d7b58d](https://github.com/ibis-project/ibis-substrait/commit/5d7b58da3b248b6874a2eb59225c2cb5335101b5))

## [2.17.0](https://github.com/ibis-project/ibis-substrait/compare/v2.16.0...v2.17.0) (2022-11-02)


### Features

* add support for manual ops.Clip ([a67713e](https://github.com/ibis-project/ibis-substrait/commit/a67713e029c3b5ca15b2c456a20529e02d436473))

## [2.16.0](https://github.com/ibis-project/ibis-substrait/compare/v2.15.0...v2.16.0) (2022-11-02)


### Features

* add support for ops.FloorDivide ([45eb64f](https://github.com/ibis-project/ibis-substrait/commit/45eb64f80e5d0f76ac38219caae48af3bfbb8d91))

## [2.15.0](https://github.com/ibis-project/ibis-substrait/compare/v2.14.1...v2.15.0) (2022-11-02)


### Features

* add support for ops.Log ([226074e](https://github.com/ibis-project/ibis-substrait/commit/226074e20648419c831d46971e3e630818ae063a))

## [2.14.1](https://github.com/ibis-project/ibis-substrait/compare/v2.14.0...v2.14.1) (2022-11-01)


### Bug Fixes

* **python:** relax python upper bound ([93215da](https://github.com/ibis-project/ibis-substrait/commit/93215da2a17a7192f34eea1c7f937f72c23d9118))

## [2.14.0](https://github.com/ibis-project/ibis-substrait/compare/v2.13.1...v2.14.0) (2022-10-25)


### Features

* allow source tables other than `UnboundTable` ([22d90f1](https://github.com/ibis-project/ibis-substrait/commit/22d90f126191ea66bf87097f7d3a750b846ca306))

## [2.13.1](https://github.com/ibis-project/ibis-substrait/compare/v2.13.0...v2.13.1) (2022-10-19)


### Bug Fixes

* **projection:** use emit and not project for column selection ([489beb8](https://github.com/ibis-project/ibis-substrait/commit/489beb87f5cc1f89d396f25a7530e89a7cc20a55))
* **ScalarFunction:** add (currently) required error enum ([135320b](https://github.com/ibis-project/ibis-substrait/commit/135320bb6da8e3a3eb2742692348f895afcdc99c))

## [2.13.0](https://github.com/ibis-project/ibis-substrait/compare/v2.12.3...v2.13.0) (2022-10-18)


### Features

* support kwargs in compile ([eba2ae3](https://github.com/ibis-project/ibis-substrait/commit/eba2ae35d97591cb429c6a71184c98fce8242816))

## [2.12.3](https://github.com/ibis-project/ibis-substrait/compare/v2.12.2...v2.12.3) (2022-10-18)


### Bug Fixes

* **3.x:** ignore missing ops when generating inverse mapping ([01248b0](https://github.com/ibis-project/ibis-substrait/commit/01248b017c42df09cfe5a5aa0a9ee8f0bad3c7b1))

## [2.12.2](https://github.com/ibis-project/ibis-substrait/compare/v2.12.1...v2.12.2) (2022-10-13)


### Bug Fixes

* re-pin protobuf, regenerate stubs, disable renovate ([3021502](https://github.com/ibis-project/ibis-substrait/commit/3021502dfaa256bd24ab49d15269c57b65d532f9))

## [2.12.1](https://github.com/ibis-project/ibis-substrait/compare/v2.12.0...v2.12.1) (2022-10-13)


### Bug Fixes

* dont set nullable=True for Literals ([681576e](https://github.com/ibis-project/ibis-substrait/commit/681576ef473e125e091cfaeffad2bdc1c838426d))

## [2.12.0](https://github.com/ibis-project/ibis-substrait/compare/v2.11.2...v2.12.0) (2022-10-13)


### Features

* add dispatch for ops.Where ([9144cf1](https://github.com/ibis-project/ibis-substrait/commit/9144cf14547fb3d7b336f8618254d67d92132a30))

## [2.11.2](https://github.com/ibis-project/ibis-substrait/compare/v2.11.1...v2.11.2) (2022-10-13)


### Bug Fixes

* **deps:** update dependency protobuf to v3.20.3 ([b11ca0d](https://github.com/ibis-project/ibis-substrait/commit/b11ca0db0aa1bed33a5f9b3c14318fe3c887d969))

## [2.11.1](https://github.com/ibis-project/ibis-substrait/compare/v2.11.0...v2.11.1) (2022-10-13)


### Bug Fixes

* **deps:** update dependency protobuf to v3.20.2 [security] ([d45f239](https://github.com/ibis-project/ibis-substrait/commit/d45f2399cd19b5014a0de1deb74abbdbd3a24aa7))

## [2.11.0](https://github.com/ibis-project/ibis-substrait/compare/v2.10.2...v2.11.0) (2022-10-12)


### Features

* add more mappings for ibis ops and substrait scalar functions ([abbdf13](https://github.com/ibis-project/ibis-substrait/commit/abbdf130ec2ed6b4491709614cd09ca0744f888e))


### Bug Fixes

* reformat with black ([37924ec](https://github.com/ibis-project/ibis-substrait/commit/37924eca9bbc4c786723ac949696d1e99fbf0f27))

## [2.10.2](https://github.com/ibis-project/ibis-substrait/compare/v2.10.1...v2.10.2) (2022-09-23)


### Bug Fixes

* invalid syntax in pyproject.toml ([24691b1](https://github.com/ibis-project/ibis-substrait/commit/24691b1e5970df8f793e41eba05a04b9d6fc5e75))

## [2.10.1](https://github.com/ibis-project/ibis-substrait/compare/v2.10.0...v2.10.1) (2022-08-27)


### Bug Fixes

* **joins:** compute field offsets for nested joins ([9f7177e](https://github.com/ibis-project/ibis-substrait/commit/9f7177e71c826294a4af9ddb5870954fb9356e5d))

## [2.10.0](https://github.com/ibis-project/ibis-substrait/compare/v2.9.8...v2.10.0) (2022-08-10)


### Features

* add dispatch rule for `FixedChar` ([24508f6](https://github.com/ibis-project/ibis-substrait/commit/24508f6ca9d365cd29feb641c02d34629a49ef82))

## [2.9.8](https://github.com/ibis-project/ibis-substrait/compare/v2.9.7...v2.9.8) (2022-08-10)


### Bug Fixes

* always calculate child rel field offsets for join predicates ([f8f7f96](https://github.com/ibis-project/ibis-substrait/commit/f8f7f96946e79bf701f17ab103a087e1ed8e85c2))

## [2.9.7](https://github.com/ibis-project/ibis-substrait/compare/v2.9.6...v2.9.7) (2022-08-09)


### Bug Fixes

* **deps:** update dependency protobuf to v3.20.1 ([24487e0](https://github.com/ibis-project/ibis-substrait/commit/24487e042c5f4330e1e4862c6818d043846988ad))

## [2.9.6](https://github.com/ibis-project/ibis-substrait/compare/v2.9.5...v2.9.6) (2022-08-09)


### Bug Fixes

* add `VarChar` to the `_decompile_field` dispatcher ([30e1daa](https://github.com/ibis-project/ibis-substrait/commit/30e1daab51744606ae481a171d7c82f79bf52dde))

## [2.9.5](https://github.com/ibis-project/ibis-substrait/compare/v2.9.4...v2.9.5) (2022-08-01)


### Bug Fixes

* **translate:** use FunctionArgument in ops.Count translation ([77ea1fa](https://github.com/ibis-project/ibis-substrait/commit/77ea1fafeb08d79a4ac54c6744247c497e33a193))

## [2.9.4](https://github.com/ibis-project/ibis-substrait/compare/v2.9.3...v2.9.4) (2022-07-27)


### Bug Fixes

* add backcompat for older ibises ([1298c1f](https://github.com/ibis-project/ibis-substrait/commit/1298c1f6f8de5481ac61410d24d4e85665856a22))

## [2.9.3](https://github.com/ibis-project/ibis-substrait/compare/v2.9.2...v2.9.3) (2022-07-21)


### Bug Fixes

* **substrait:** update substrait to version 0.8 ([c06a9b5](https://github.com/ibis-project/ibis-substrait/commit/c06a9b5dfd1c09f0b5e05b456da9569038cb420a))

## [2.9.2](https://github.com/ibis-project/ibis-substrait/compare/v2.9.1...v2.9.2) (2022-06-30)


### Bug Fixes

* translate all literals as nullable ([3453469](https://github.com/ibis-project/ibis-substrait/commit/34534696d507bbd0b2b232e208730c2566d8225c))

## [2.9.1](https://github.com/ibis-project/ibis-substrait/compare/v2.9.0...v2.9.1) (2022-06-29)


### Bug Fixes

* **extract:** substrait function argument ordering ([beca56c](https://github.com/ibis-project/ibis-substrait/commit/beca56cfd3c336dd1572009b5fda978f5ff4945c))

## [2.9.0](https://github.com/ibis-project/ibis-substrait/compare/v2.8.0...v2.9.0) (2022-06-28)


### Features

* add support for ops.Extract<span> ([2fe7f26](https://github.com/ibis-project/ibis-substrait/commit/2fe7f26aa7efce33462cdc9fddc629ccce9183f7))

## [2.8.0](https://github.com/ibis-project/ibis-substrait/compare/v2.7.0...v2.8.0) (2022-06-27)


### Features

* add ops.SearchedCase handling ([be13d4c](https://github.com/ibis-project/ibis-substrait/commit/be13d4cc55e2ae7d2506abde8c400a99439a3e6f))

## [2.7.0](https://github.com/ibis-project/ibis-substrait/compare/v2.6.0...v2.7.0) (2022-05-14)


### Features

* add ops.Cast to translator and decompiler ([911b2fd](https://github.com/ibis-project/ibis-substrait/commit/911b2fd25d742d2c035057e8907104dc2e42d50f))

## [2.6.0](https://github.com/ibis-project/ibis-substrait/compare/v2.5.0...v2.6.0) (2022-05-13)


### Features

* add ops.Contains -> singular_or_list translation ([d768ea3](https://github.com/ibis-project/ibis-substrait/commit/d768ea32ec1dbe92121f5dd3a3e1a0e568a34f1a))

## [2.5.0](https://github.com/ibis-project/ibis-substrait/compare/v2.4.0...v2.5.0) (2022-05-12)


### Features

* add ops.SimpleCase to translate and decompile ([a12b4e3](https://github.com/ibis-project/ibis-substrait/commit/a12b4e3e3060fa06b191258dae686ecb80f0d4c8))

## [2.4.0](https://github.com/ibis-project/ibis-substrait/compare/v2.3.2...v2.4.0) (2022-05-12)


### Features

* **struct:** add struct field access ([26c329a](https://github.com/ibis-project/ibis-substrait/commit/26c329a8c5398bd161524b0d45c874a15045f15f))

### [2.3.2](https://github.com/ibis-project/ibis-substrait/compare/v2.3.1...v2.3.2) (2022-05-12)


### Bug Fixes

* **deps:** pin protobuf to 3.19 ([a448875](https://github.com/ibis-project/ibis-substrait/commit/a448875e17625c8e8d90c09d7a4652911b2c7319))

### [2.3.1](https://github.com/ibis-project/ibis-substrait/compare/v2.3.0...v2.3.1) (2022-05-11)


### Bug Fixes

* **deps:** update dependency platformdirs to <2.5.3 ([43030e4](https://github.com/ibis-project/ibis-substrait/commit/43030e4a906972df86621b1598f99326630094e1))

## [2.3.0](https://github.com/ibis-project/ibis-substrait/compare/v2.2.1...v2.3.0) (2022-05-11)


### Features

* add mappings for ibis ops <-> substrait scalar functions ([dc81c58](https://github.com/ibis-project/ibis-substrait/commit/dc81c582f3e4b07e44c943998401fd6db5516e5b))


### Bug Fixes

* bring ibis-substrait in line spec as per validator ([fc000bb](https://github.com/ibis-project/ibis-substrait/commit/fc000bbe4165494417e872a566d70d12b25f0a47))
* dispatch underlying op for aliases and decimal literal ([66e93e1](https://github.com/ibis-project/ibis-substrait/commit/66e93e156c98f3bb3024124fb62b3533a02c4895))
* use `isoformat` for creating date literal ([c8d008f](https://github.com/ibis-project/ibis-substrait/commit/c8d008f415137e15f858459149cf7122ac8a1362))

### [2.2.1](https://github.com/ibis-project/ibis-substrait/compare/v2.2.0...v2.2.1) (2022-05-11)


### Bug Fixes

* **version:** add version to dunder init ([cf3040c](https://github.com/ibis-project/ibis-substrait/commit/cf3040c02c47485f8d34161bd4adde357d285eaa))

# [2.2.0](https://github.com/ibis-project/ibis-substrait/compare/v2.1.0...v2.2.0) (2022-05-11)


### Features

* **compiler:** expand table expression to its columns ([abbdf19](https://github.com/ibis-project/ibis-substrait/commit/abbdf194dc551ac5844aa5570ab58eabeb3cbb22))

# [2.1.0](https://github.com/ibis-project/ibis-substrait/compare/v2.0.0...v2.1.0) (2022-04-05)


### Features

* **compiler:** expose extension uri parameter in constructor ([7a7fee4](https://github.com/ibis-project/ibis-substrait/commit/7a7fee47d19a52510fde71af0aaa96372b18c1cb))

# [2.0.0](https://github.com/ibis-project/ibis-substrait/compare/v1.0.2...v2.0.0) (2022-02-22)


### Bug Fixes

* adjust imports for new substrait proto layout ([a5a0953](https://github.com/ibis-project/ibis-substrait/commit/a5a0953e83aeb4d9249ea97826aea0e1f8e8ed4c))


### chore

* drop Python 3.7 support ([6c13ca7](https://github.com/ibis-project/ibis-substrait/commit/6c13ca7cad3a1ef3dbd6cd7ae80dff3fdcbe6848))
* **protos:** bump substrait to latest commit ([7b1d441](https://github.com/ibis-project/ibis-substrait/commit/7b1d441e8e9e916729bc0674e83e9a6a3d88e2b2))


### BREAKING CHANGES

* **protos:** Older Substrait protos are no longer supported
* Python 3.7 is no longer supported.

## [1.0.2](https://github.com/ibis-project/ibis-substrait/compare/v1.0.1...v1.0.2) (2022-02-22)


### Bug Fixes

* fix broken field offset construction ([7c41b55](https://github.com/ibis-project/ibis-substrait/commit/7c41b555f22f01db4c57252dded07ce8c2b678bc))

## [1.0.1](https://github.com/ibis-project/ibis-substrait/compare/v1.0.0...v1.0.1) (2022-02-02)


### Bug Fixes

* **deps:** fix gen-protos script and bump protos ([3a2b01b](https://github.com/ibis-project/ibis-substrait/commit/3a2b01bad8ccd9647ba60c13956f0d4c9979588d))

# 1.0.0 (2022-01-18)


### Bug Fixes

* force reproducible poetry.lock ([cfff0c4](https://github.com/ibis-project/ibis-substrait/commit/cfff0c4fc8d08788e8959110c9db2ee34dec6c09))


### Features

* initial commit ([fd1d7e3](https://github.com/ibis-project/ibis-substrait/commit/fd1d7e3ad52b71e3c67fdf323462240bc0c9255e))

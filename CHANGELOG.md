Release Notes
---

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

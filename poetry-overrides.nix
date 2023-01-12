self: super: {
  sqlalchemy = super.sqlalchemy.override { preferWheel = !self.stdenv.isDarwin; };
}

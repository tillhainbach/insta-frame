module.exports = {
  extends: ["@commitlint/config-conventional"],

  ignores: [(commit) => commit.startsWith("[WIP]")],

  rules: {
    "scope-enum": [2, "always", ["repo", "web-app", "deploy"]],
    "scope-case": [2, "always", "kebab-case"],
    "scope-empty": [2, "never"],
  },
};

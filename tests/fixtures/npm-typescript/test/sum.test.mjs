import assert from "node:assert/strict";
import test from "node:test";

import { sum } from "../dist/sum.js";

test("sums two numbers", () => {
  assert.equal(sum(2, 3), 5);
});

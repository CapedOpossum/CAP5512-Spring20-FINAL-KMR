import unittest
from gabasic import OnePointMappingCrossover


class OnePointMappingCrossoverTest(unittest.TestCase):
  def test_mapping_keys_to_tuples(self):
    sample_1 = {
      (1, 0): 'Hello',
      (1, 1): 'There',
      (2, 0): 'People'
    }
    expected_value = [
      (1, (1, 0)),
      (1, (1, 1)),
      (1, (2, 0))
    ]
    actual_value = OnePointMappingCrossover.mapping_keys_to_tuples(1, sample_1)
    self.assertEqual(expected_value, actual_value)

  def test_mapping_deep_copy(self):
    sample_1 = {
      (1, 0): 'Hello',
      (1, 1): 'There',
      (2, 0): 'People'
    }
    the_copy = OnePointMappingCrossover.mapping_deep_copy(sample_1)
    sample_1[(1, 0)] = 'HELLO'
    self.assertEqual('HELLO', sample_1[(1, 0)])
    self.assertEqual('Hello', the_copy[(1, 0)])

  def test_blend_mapping_using_tuples(self):
    sample_1 = {
      (1, 0): 'Hello',
      (1, 1): 'There',
      (2, 0): 'People'
    }
    sample_2 = {
      (1, 1): 'To',
      (2, 0): 'The',
      (1, 0): 'Victor',
      (2, 1): 'Go',
      (1, 2): 'The',
      (2, 2): 'Spoils'
    }
    src_keys_1 = [
      (1, (1, 0)),
      (1, (1, 1)),
      (1, (2, 0))
    ]
    src_keys_2 = [
      (2, (1, 1)),
      (2, (2, 0)),
      (2, (1, 0)),
      (2, (2, 1)),
      (2, (1, 2)),
      (2, (2, 2))
    ]
    # Mimic a cross-over at key tuple index 2
    keys_1 = [
      src_keys_1[0],       # (1, 0)
      src_keys_1[1],       # (1, 1)
      src_keys_2[2],       # (1, 0) -> Collision
      src_keys_2[3],       # (2, 1)
      src_keys_2[4],       # (1, 2)
      src_keys_2[5]        # (2, 2)
    ]
    keys_2 = [
      src_keys_2[0],       # (1, 1)
      src_keys_2[1],       # (2, 0)
      src_keys_1[2]        # (2, 0) -> Collision
    ]
    # (1,0) and (2,0) key collisions should be resolved in favor of later item
    # in key array
    expected_1 = {
      (1, 1): 'There',
      (1, 0): 'Victor',
      (2, 1): 'Go',
      (1, 2): 'The',
      (2, 2): 'Spoils'
    }
    expected_2 = {
      (1, 1): 'To',
      (2, 0): 'People'
    }
    OnePointMappingCrossover.blend_mappings_using_tuples(
      sample_1,
      sample_2,
      keys_1,
      keys_2
    )
    self.assertEqual(expected_1, sample_1)
    self.assertEqual(expected_2, sample_2)

# vim: set ts=2 sw=2 expandtab:

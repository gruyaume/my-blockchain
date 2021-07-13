from node.merkle_tree import build_merkle_tree, calculate_hash


def test_given_2_leaves_when_build_merkle_tree_then_all_leaves_hashes_are_computed_correctly():
    l1 = "blabla data 0"
    l2 = "blabla data 1"
    merkle_tree = build_merkle_tree([l1, l2])

    assert merkle_tree.left_child.value == calculate_hash(l1)
    assert merkle_tree.right_child.value == calculate_hash(l2)


def test_given_2_leaves_when_build_merkle_tree_then_root_hash_is_computed_correctly():
    l1 = "blabla data 0"
    l2 = "blabla data 1"
    merkle_tree = build_merkle_tree([l1, l2])

    assert merkle_tree.value == calculate_hash(calculate_hash(l1) + calculate_hash(l2))


def test_given_4_leaves_when_build_merkle_tree_then_all_leaves_hashes_are_computed_correctly():
    l1 = "blabla data 0"
    l2 = "blabla data 1"
    l3 = "blabla data 2"
    l4 = "blabla data 3"
    merkle_tree = build_merkle_tree([l1, l2, l3, l4])

    assert merkle_tree.left_child.left_child.value == calculate_hash(l1)
    assert merkle_tree.left_child.right_child.value == calculate_hash(l2)
    assert merkle_tree.right_child.left_child.value == calculate_hash(l3)
    assert merkle_tree.right_child.right_child.value == calculate_hash(l4)


def test_given_4_leaves_when_build_merkle_tree_then_middle_childs_are_computed_correctly():
    l1 = "blabla data 0"
    l2 = "blabla data 1"
    l3 = "blabla data 2"
    l4 = "blabla data 3"
    merkle_tree = build_merkle_tree([l1, l2, l3, l4])

    assert merkle_tree.left_child.value == calculate_hash(calculate_hash(l1)+calculate_hash(l2))
    assert merkle_tree.right_child.value == calculate_hash(calculate_hash(l3)+calculate_hash(l4))


def test_given_4_leaves_when_build_merkle_tree_then_root_is_computed_correctly():
    l1 = "blabla data 0"
    l2 = "blabla data 1"
    l3 = "blabla data 2"
    l4 = "blabla data 3"
    merkle_tree = build_merkle_tree([l1, l2, l3, l4])

    assert merkle_tree.value == calculate_hash(calculate_hash(calculate_hash(l1)+calculate_hash(l2))+calculate_hash(calculate_hash(l3)+calculate_hash(l4)))


def test_given_6_leaves_when_build_merkle_tree_then_all_leaves_hashes_are_computed_correctly():
    l1 = "blabla data 0"
    l2 = "blabla data 1"
    l3 = "blabla data 2"
    l4 = "blabla data 3"
    l5 = "blabla data 4"
    l6 = "blabla data 5"
    merkle_tree = build_merkle_tree([l1, l2, l3, l4, l5, l6])

    assert merkle_tree.left_child.left_child.left_child.value == calculate_hash(l1)
    assert merkle_tree.left_child.left_child.right_child.value == calculate_hash(l2)
    assert merkle_tree.left_child.right_child.left_child.value == calculate_hash(l3)
    assert merkle_tree.left_child.right_child.right_child.value == calculate_hash(l4)
    assert merkle_tree.right_child.left_child.left_child.value == calculate_hash(l5)
    assert merkle_tree.right_child.left_child.right_child.value == calculate_hash(l6)
    assert merkle_tree.right_child.right_child.left_child.value == calculate_hash(l5)
    assert merkle_tree.right_child.right_child.right_child.value == calculate_hash(l6)


def test_given_6_leaves_when_build_merkle_tree_then_root_is_computed_correctly():
    l1 = "blabla data 0"
    l2 = "blabla data 1"
    l3 = "blabla data 2"
    l4 = "blabla data 3"
    l5 = "blabla data 4"
    l6 = "blabla data 5"
    merkle_tree = build_merkle_tree([l1, l2, l3, l4, l5, l6])

    assert merkle_tree.value == calculate_hash(calculate_hash(calculate_hash(calculate_hash(l1)+calculate_hash(l2))+calculate_hash(calculate_hash(l3)+calculate_hash(l4))) + calculate_hash(calculate_hash(calculate_hash(l5)+calculate_hash(l6))+calculate_hash(calculate_hash(l5)+calculate_hash(l6))))


def test_given_5_leaves_when_build_merkle_tree_then_all_leaves_hashes_are_computed_correctly():
    l1 = "blabla data 0"
    l2 = "blabla data 1"
    l3 = "blabla data 2"
    l4 = "blabla data 3"
    l5 = "blabla data 4"
    merkle_tree = build_merkle_tree([l1, l2, l3, l4, l5])

    assert merkle_tree.left_child.left_child.left_child.value == calculate_hash(l1)
    assert merkle_tree.left_child.left_child.right_child.value == calculate_hash(l2)
    assert merkle_tree.left_child.right_child.left_child.value == calculate_hash(l3)
    assert merkle_tree.left_child.right_child.right_child.value == calculate_hash(l4)
    assert merkle_tree.right_child.left_child.left_child.value == calculate_hash(l5)
    assert merkle_tree.right_child.left_child.right_child.value == calculate_hash(l5)
    assert merkle_tree.right_child.right_child.left_child.value == calculate_hash(l5)
    assert merkle_tree.right_child.right_child.right_child.value == calculate_hash(l5)


def test_given_5_leaves_when_build_merkle_tree_then_root_is_computed_correctly():
    l1 = "blabla data 0"
    l2 = "blabla data 1"
    l3 = "blabla data 2"
    l4 = "blabla data 3"
    l5 = "blabla data 4"
    merkle_tree = build_merkle_tree([l1, l2, l3, l4, l5])

    assert merkle_tree.value == calculate_hash(calculate_hash(calculate_hash(calculate_hash(l1)+calculate_hash(l2))+calculate_hash(calculate_hash(l3)+calculate_hash(l4))) + calculate_hash(calculate_hash(calculate_hash(l5)+calculate_hash(l5))+calculate_hash(calculate_hash(l5)+calculate_hash(l5))))

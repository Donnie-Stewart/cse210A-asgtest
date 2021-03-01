datatype Tree<T> = Leaf | Node(Tree<T>, Tree<T>, T)
datatype List<T> = Nil | Cons(T, List<T>)

function flatten<T>(tree:Tree<T>):List<T>
        ensures tree == Leaf ==> flatten(tree) == Nil 
        decreases tree
{
	match tree
        case Leaf => Nil
        case Node(left, right, t) => Cons(t, append(flatten(left), flatten(right)))
}

function append<T>(xs:List<T>, ys:List<T>):List<T>
        ensures xs == Nil ==> append(xs, ys) == ys
        ensures ys == Nil ==> append(xs, ys) == xs
        decreases xs 
{
        match xs
        case Nil => ys
        case Cons(x, xs') => Cons(x, append(xs', ys))
	
}

function treeContains<T>(tree:Tree<T>, element:T):bool
        ensures tree == Leaf ==> treeContains(tree,element) == false
        ensures tree == Node(tree,tree,element) ==> treeContains(tree,element) == false || treeContains(tree,element) == true
{
        match tree
        case Leaf => false 
        case Node(left, right, t) => listContains(flatten(tree),element)
}

function listContains<T>(xs:List<T>, element:T):bool
        ensures xs == Nil ==> listContains(xs, element) == false
        decreases xs
{
        match xs
        case Nil => false
        case Cons(x, xs') => (x == element) || listContains(xs', element)
}


lemma sameElements<T>(tree:Tree<T>, element:T)
ensures treeContains(tree, element) <==> listContains(flatten(tree), element)
{
	match tree
        case Leaf => {
                assert treeContains(Leaf,element)
                == false 
                ;
        } 
        case Node(left, right, t) => {
                assert treeContains(Node(left, right, t), element)
                == treeContains(left,element) || treeContains(right,element) || (t == element)
                == listContains(flatten(left),element) || listContains(flatten(right),element) || (t == element)
                == listContains(append(flatten(left),flatten(right)),element) || (t == element)
                == listContains(Cons(t, append(flatten(left), flatten(right))),element)
                == listContains(flatten(tree), element)
                ;
        }
}
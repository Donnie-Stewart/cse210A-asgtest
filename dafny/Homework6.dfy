datatype Tree<T> = Leaf | Node(Tree<T>, Tree<T>, T)
datatype List<T> = Nil | Cons(T, List<T>)

function flatten<T>(tree:Tree<T>):List<T>
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
{
	match tree
        case Leaf => false 
        case Node(left, right, t) => listContains(flatten(tree),element)
}

function listContains<T>(xs:List<T>, element:T):bool
ensures xs == Nil ==> listContains(xs, element) == false
decreases xs
// ensures T >= 0
{
    match xs
        case Nil => false
        case Cons(x, xs') => (x == element) || listContains(xs', element)
}


// lemma sameElements<T>(tree:Tree<T>, element:T)
// ensures treeContains(tree, element) <==> listContains(flatten(tree), element)
// {
	

datatype Tree<T> = Leaf | Node(Tree<T>, Tree<T>, T)
datatype List<T> = Nil | Cons(T, List<T>)

function flatten<T>(tree:Tree<T>):List<T>
decreases tree
{
	match tree
        case Leaf => Nil
        case Node(left, right, t) => Cons(t, append(flatten(left), flatten(right)))
}

function method append<T>(xs:List<T>, ys:List<T>):List<T>
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

function method listContains<T(==)>(xs:List<T>, element:T):bool
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
	
// }
method Main()
{
var list:List;
list := Cons(0, Cons(5, Nil));
print "list1=", list, "\n";
var list2:List;
list2 := Cons(1, Cons(2, Nil));

// list := Cons(5, list);
// var list2 := Nil;
// list2 := Cons(0, list);
// list2 := Cons(8, list);
var list3:List := append(list, list2);
print "list3=", list3, "\n";
// var x : Tree := Node(Node(Empty, 1, Empty), 2, Empty);
// print "x=", m, "\n";
// assert m == 4;

print "t_f: ", listContains(list3, 2), "\n";
    

}
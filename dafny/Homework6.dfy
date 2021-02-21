datatype Tree<T> = Leaf | Node(Tree<T>, Tree<T>, T)
datatype List<T> = Nil | Cons(T, List<T>)

// function flatten<T>(tree:Tree<T>):List<T>
// {
	
// }
function method length <T>(xs:List<T>): int
ensures length(xs) >= 0
ensures xs == Nil ==> length(xs) == 0
{
    match xs
        case Nil =>0
        case Cons(x,xs') => 1+length(xs')
}


function method append<T>(xs:List<T>, ys:List<T>):List<T>
ensures xs == Nil ==> append(xs, ys) == ys
ensures ys == Nil ==> append(xs, ys) == xs
ensures length(append(xs, ys)) == length(xs) + length(ys)
{
    match xs
        case Nil => ys
        case Cons(x, xs') => Cons(x, append(xs', ys))
	
}

// function treeContains<T>(tree:Tree<T>, element:T):bool
// {
	
// }

// function listContains<T>(xs:List<T>, element:T):bool
// {
	
// }


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
print "length", length(list3), "\n";
// var x : Tree := Node(Node(Empty, 1, Empty), 2, Empty);
// print "x=", m, "\n";
// assert m == 4;


    

}
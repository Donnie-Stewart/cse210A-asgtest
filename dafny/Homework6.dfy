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
        decreases tree 
{
        match tree
        case Leaf => false 
        case Node(left, right, t) => (t==element) || treeContains(left,element) || treeContains(right,element)
}

function listContains<T>(xs:List<T>, element:T):bool
        ensures xs == Nil ==> listContains(xs, element) == false
        decreases xs
{
        match xs
        case Nil => false
        case Cons(x, xs') => (x == element) || listContains(xs', element)
}

lemma appendListContains<T>(xs:List<T>,ys:List<T>,element:T)
ensures listContains(xs,element) || listContains(ys,element) <==> listContains(append(xs,ys),element)
        decreases xs 
        decreases ys 
{
        match xs
        case Nil => {
                // assert listContains(Nil,element) || listContains(ys,element)
                // == false || listContains(ys,element)
                // == listContains(ys,element)
                // == listContains(append(Nil,ys),element)
                // ;
        }
        case Cons(x,xs') => {

                appendListContains(xs',ys, element);

                assert listContains(xs,element) || listContains(ys,element)
                == listContains(Cons(x,xs'),element) || listContains(ys,element)
                == (x == element) || listContains(xs',element) || listContains(ys,element)
                == (x == element) || listContains(append(xs',ys),element)
                == listContains(Cons(x,append(xs',ys)),element)
                == listContains(append(Cons(x,xs'),ys),element)
                == listContains(append(xs,ys),element)
                ;
        }
}

lemma sameElements<T>(tree:Tree<T>, element:T)
ensures treeContains(tree, element) <==> listContains(flatten(tree), element)
decreases tree 
{
	match tree
        case Leaf => {} 
        case Node(left, right, t) => {
                sameElements(left,element);
                sameElements(right,element);
                appendListContains(flatten(left),flatten(right),element);

                assert treeContains(Node(left, right, t), element)
                == treeContains(left,element) || treeContains(right,element) || (t == element)
                == listContains(flatten(left),element) || listContains(flatten(right),element) || (t == element)
                == listContains(append(flatten(left),flatten(right)),element) || (t == element)
                == listContains(Cons(t, append(flatten(left), flatten(right))),element)
                == listContains(flatten(tree), element)
                ;
        }
}
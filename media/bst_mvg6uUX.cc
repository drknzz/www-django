#include<bits/stdc++.h>
using namespace std;

typedef struct node BST;
struct node {
    int key;
    BST* left;
    BST* right;
};

BST* search(BST* root, int key) { 
    if (!root || root->key == key) 
       return root; 
     
    if (root->key < key) 
       return search(root->right, key); 
  
    return search(root->left, key); 
}

BST* insert(BST* root, int value) { 
    if (!root) {
        BST* node = new BST;
        node->key = value;
        node->left = nullptr;
        node->right = nullptr;
        return node;
    }
  
    if (value > root->key) { 
        root->right = insert(root->right, value); 
    }
    else { 
        root->left = insert(root->left, value); 
    } 
  
    return root; 
} 
  
void inorder(BST* root) { 
    if (!root)
        return; 

    inorder(root->left);
    cout << root->key << "\n";
    inorder(root->right); 
}

int main() {
    BST* r = new BST;
    r->key = 3;
    r->left = r->right = nullptr;

    insert(r, 5);
    insert(r, 0);
    insert(r, 2);
    insert(r, 1);
    insert(r, 4);

    inorder(r);
}

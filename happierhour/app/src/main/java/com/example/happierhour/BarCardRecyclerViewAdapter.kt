package com.example.happierhour

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView

//class BarCardRecyclerViewAdapter(private val productList: List<Bar_Model>) : RecyclerView.Adapter<ProductCardViewHolder>() {
//
//    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ProductCardViewHolder {
//        val layoutView = LayoutInflater.from(parent.context).inflate(R.layout.shr_product_card, parent, false)
//        return ProductCardViewHolder(layoutView)
//    }
//
//    override fun onBindViewHolder(holder: ProductCardViewHolder, position: Int) {
//        // TODO: Put ViewHolder binding code here in MDC-102
//        if (position < productList.size) {
//            val product = productList[position]
//            holder.productTitle.text = product.title
//            holder.productPrice.text = product.price
//            ImageRequester.setImageFromUrl(holder.productImage, product.url)
//
//        }
//    }
//    override fun getItemCount(): Int {
//        return productList.size
//    }
//}
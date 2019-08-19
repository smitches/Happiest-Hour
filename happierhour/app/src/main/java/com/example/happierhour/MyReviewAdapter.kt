package com.example.happierhour

import android.app.Activity
import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.TextView

class MyReviewAdapter (private var activity: Activity, private var items: ArrayList<Review_Model>) :  BaseAdapter(){

    private class ViewHolder(row: View?) {
        var lblRating: TextView? = null
        var lblReviewer: TextView? = null
        var lblText: TextView? = null

        init {
            this.lblRating = row?.findViewById<TextView>(R.id.lbl_rating)
            this.lblReviewer = row?.findViewById<TextView>(R.id.lbl_reviewer)
            this.lblText = row?.findViewById<TextView>(R.id.lbl_text)
        }
    }
    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
        val view: View
        val viewHolder: ViewHolder
        if (convertView == null) {
            val inflater = activity?.getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater
            view = inflater.inflate(R.layout.single_review, null)
            viewHolder = ViewHolder(view)
            view.tag = viewHolder
        } else {
            view = convertView
            viewHolder = view.tag as ViewHolder
        }
        var r = items[position]
        viewHolder.lblRating?.text = r.star_count
        viewHolder.lblReviewer?.text = r.reviewer.first_name
        viewHolder.lblText?.text = r.review_text

        return view as View
    }
    override fun getItem(i: Int): Review_Model {
        return items[i]
    }
    override fun getItemId(i: Int): Long {
        return i.toLong()
    }
    override fun getCount(): Int {
        return items.size
    }
}
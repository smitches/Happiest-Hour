package com.example.happierhour

import androidx.coordinatorlayout.widget.CoordinatorLayout.Behavior.setTag
import android.view.animation.AnimationUtils.loadAnimation
import android.view.animation.Animation
import android.widget.TextView
import android.R.attr.name
import android.app.Activity
import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import com.google.android.material.snackbar.Snackbar
import android.widget.ArrayAdapter
import android.widget.BaseAdapter
import android.widget.ImageView
import androidx.recyclerview.widget.RecyclerView
import androidx.recyclerview.widget.RecyclerView.ViewHolder


class BarCardListViewAdapter (private var activity: Activity, private var items: ArrayList<Bar_Model>) :  BaseAdapter() {
    private class ViewHolder(row: View?) {
        var lblName: TextView? = null
//        var lblDesignation: TextView? = null
//        var imgEmp: ImageView? = null
//        var lblSalary: TextView? = null

        init {
            this.lblName = row?.findViewById(R.id.lbl_name)
            this.lblName = row?.findViewById<TextView>(R.id.lbl_name)
//            this.lblDesignation = row?.findViewById<TextView>(R.id.lbl_designation)
//            this.imgEmp = row?.findViewById<ImageView>(R.id.img_emp)
//            this.lblSalary = row?.findViewById<TextView>(R.id.lbl_salary)
        }
    }
    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
        val view: View
        val viewHolder: ViewHolder
        if (convertView == null) {
            val inflater = activity?.getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater
            view = inflater.inflate(R.layout.bar_card, null)
            viewHolder = ViewHolder(view)
            view.tag = viewHolder
        } else {
            view = convertView
            viewHolder = view.tag as ViewHolder
        }
        var bar = items[position]
        viewHolder.lblName?.text = bar.bar_name
//        viewHolder.lblDesignation?.text = emp.emp_designation
//        viewHolder.lblSalary?.text = emp.emp_salary
//        viewHolder.imgEmp?.setImageResource(emp.emp_photo!!)

        return view as View
    }


    override fun getItem(i: Int): Bar_Model {
        return items[i]
    }

    override fun getItemId(i: Int): Long {
        return i.toLong()
    }

    override fun getCount(): Int {
        return items.size
    }
}
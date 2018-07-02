package utec.dbp.mychat;

import android.content.Context;
import android.content.Intent;
import android.support.annotation.NonNull;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class MyMessageAdapter extends RecyclerView.Adapter<MyMessageAdapter.ViewHolder>  {
    public JSONArray elements;
    private Context mContext;
    private int cursoId;
    private static final String TAG = "MyMessageAdapter";

    public MyMessageAdapter(JSONArray elements, Context context, int cursoId) {
        this.elements = elements;
        this.mContext = context;
        this.cursoId = cursoId;
    }

    public class ViewHolder extends RecyclerView.ViewHolder {
        TextView first_line;
        TextView second_line;
        RelativeLayout container;

        public ViewHolder(View itemView) {
            super(itemView);
            first_line = itemView.findViewById(R.id.element_view_first_line);
            second_line = itemView.findViewById(R.id.element_view_second_line);
            container = itemView.findViewById(R.id.element_view_container);
        }
    }

    @NonNull
    @Override
    public MyMessageAdapter.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        Log.d(TAG, "onCreateViewHolder: ");
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.message_view, parent, false);
        return new MyMessageAdapter.ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull MyMessageAdapter.ViewHolder holder, int position) {
        try {
            final JSONObject element = elements.getJSONObject(position);
            final String mFirstLine = element.getString("variable")+" "+element.getString("nota");
            final String mSecondLine = element.getString("porcentaje")+"%";
            final String id = element.getString("id");

            holder.first_line.setText(mFirstLine);
            holder.second_line.setText(mSecondLine);

            /*holder.container.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    String text = mFirstLine + ": " + mSecondLine;
                    Intent intent = new Intent(mContext, MessageActivity.class);
                    intent.putExtra(MessageActivity.EXTRA_USER_FROM_ID, userFromId);
                    intent.putExtra(MessageActivity.EXTRA_USER_TO_ID, id);
                    mContext.startActivity(intent);
                    Toast.makeText(mContext, text+":"+userFromId+"--"+id, Toast.LENGTH_SHORT).show();
                }
            });*/
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Override
    public int getItemCount() {
        return elements.length();
    }
}

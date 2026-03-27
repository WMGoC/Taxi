package com.example.taxidriver; // ЗАМЕНИТЕ НА ВАШ ПАКЕТ

import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MainActivity extends AppCompatActivity {

    private ListView ordersListView;
    private Button refreshButton;
    private Button btnNew, btnAssigned, btnInProgress, btnCompleted;
    private TextView titleStatus;

    private List<String> ordersList;
    private ArrayAdapter<String> ordersAdapter;
    private List<JSONObject> ridesData;
    private ExecutorService executorService;

    private String currentStatus = "new"; // new, assigned, in_progress, completed

    // !!! ВАЖНО: Замените IP на IP вашего компьютера !!!
    private final String BASE_URL = "http://192.168.1.67/taxi_api/";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ordersListView = findViewById(R.id.ordersListView);
        refreshButton = findViewById(R.id.refreshButton);
        btnNew = findViewById(R.id.btnNew);
        btnAssigned = findViewById(R.id.btnAssigned);
        btnInProgress = findViewById(R.id.btnInProgress);
        btnCompleted = findViewById(R.id.btnCompleted);
        titleStatus = findViewById(R.id.titleStatus);

        ordersList = new ArrayList<>();
        ridesData = new ArrayList<>();
        executorService = Executors.newSingleThreadExecutor();

        ordersAdapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_list_item_1,
                ordersList) {
            @Override
            public View getView(int position, View convertView, android.view.ViewGroup parent) {
                View view = super.getView(position, convertView, parent);
                android.widget.TextView textView = (android.widget.TextView) view;
                textView.setTextColor(android.graphics.Color.WHITE);
                textView.setTextSize(14);
                textView.setPadding(16, 16, 16, 16);
                return view;
            }
        };
        ordersListView.setAdapter(ordersAdapter);

        btnNew.setOnClickListener(v -> {
            currentStatus = "new";
            titleStatus.setText("🟢 Новые заказы:");
            loadOrders();
            highlightActiveButton(btnNew);
        });

        btnAssigned.setOnClickListener(v -> {
            currentStatus = "assigned";
            titleStatus.setText("🟡 Назначенные заказы:");
            loadOrders();
            highlightActiveButton(btnAssigned);
        });

        btnInProgress.setOnClickListener(v -> {
            currentStatus = "in_progress";
            titleStatus.setText("🟠 Заказы в пути:");
            loadOrders();
            highlightActiveButton(btnInProgress);
        });

        btnCompleted.setOnClickListener(v -> {
            currentStatus = "completed";
            titleStatus.setText("✅ Выполненные заказы:");
            loadOrders();
            highlightActiveButton(btnCompleted);
        });

        refreshButton.setOnClickListener(v -> {
            loadOrders();
        });

        ordersListView.setOnItemClickListener((parent, view, position, id) -> {
            JSONObject order = ridesData.get(position);
            showOrderDetails(order);
        });

        loadOrders();
        highlightActiveButton(btnNew);
    }

    private void highlightActiveButton(Button activeButton) {
        // Сброс всех кнопок - устанавливаем серый фон
        btnNew.setBackgroundColor(ContextCompat.getColor(this, android.R.color.darker_gray));
        btnAssigned.setBackgroundColor(ContextCompat.getColor(this, android.R.color.darker_gray));
        btnInProgress.setBackgroundColor(ContextCompat.getColor(this, android.R.color.darker_gray));
        btnCompleted.setBackgroundColor(ContextCompat.getColor(this, android.R.color.darker_gray));

        // Подсветка активной кнопки - оранжевый цвет
        activeButton.setBackgroundColor(ContextCompat.getColor(this, android.R.color.holo_orange_dark));
    }

    private void showOrderDetails(JSONObject order) {
        try {
            int id = order.getInt("id");
            String startAddress = order.getString("start_address");
            String endAddress = order.getString("end_address");
            String status = order.getString("status");
            String driverName = order.optString("driver_name", "Не назначен");
            String clientName = order.optString("client_name", "Не указан");
            String clientPhone = order.optString("client_phone", "Не указан");
            String createdAt = order.optString("created_at", "");
            String completedAt = order.optString("completed_at", "");

            // Переводим статус на русский
            String statusRu;
            switch (status) {
                case "new":
                    statusRu = "🟢 НОВЫЙ";
                    break;
                case "assigned":
                    statusRu = "🟡 НАЗНАЧЕН";
                    break;
                case "in_progress":
                    statusRu = "🟠 В ПУТИ";
                    break;
                case "completed":
                    statusRu = "✅ ВЫПОЛНЕН";
                    break;
                default:
                    statusRu = status;
            }

            // Формируем сообщение
            StringBuilder details = new StringBuilder();
            details.append("📋 ЗАКАЗ #").append(id).append("\n\n");
            details.append("Статус: ").append(statusRu).append("\n\n");
            details.append("👤 Клиент: ").append(clientName).append("\n");
            details.append("📞 Телефон: ").append(clientPhone).append("\n\n");
            details.append("📍 Откуда: ").append(startAddress).append("\n");
            details.append("🏁 Куда: ").append(endAddress).append("\n\n");
            details.append("🚗 Водитель: ").append(driverName).append("\n");
            details.append("📅 Создан: ").append(createdAt).append("\n");
            if (!completedAt.isEmpty() && !completedAt.equals("null")) {
                details.append("✅ Завершен: ").append(completedAt);
            }

            // Показываем диалог
            new AlertDialog.Builder(this)
                    .setTitle("Детали заказа #" + id)
                    .setMessage(details.toString())
                    .setPositiveButton("Закрыть", null)
                    .show();

        } catch (Exception e) {
            Toast.makeText(this, "Ошибка: " + e.getMessage(), Toast.LENGTH_SHORT).show();
        }
    }

    private void loadOrders() {
        refreshButton.setEnabled(false);
        refreshButton.setText("Загрузка...");

        executorService.execute(() -> {
            try {
                String urlString = BASE_URL + "get_orders.php?status=" + currentStatus;
                URL url = new URL(urlString);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(5000);

                BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream(), "UTF-8"));
                StringBuilder result = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    result.append(line);
                }
                reader.close();
                conn.disconnect();

                JSONArray ordersArray = new JSONArray(result.toString());
                ridesData.clear();
                ordersList.clear();

                for (int i = 0; i < ordersArray.length(); i++) {
                    JSONObject obj = ordersArray.getJSONObject(i);
                    ridesData.add(obj);

                    String status = obj.getString("status");
                    String statusIcon;
                    switch (status) {
                        case "new":
                            statusIcon = "🟢";
                            break;
                        case "assigned":
                            statusIcon = "🟡";
                            break;
                        case "in_progress":
                            statusIcon = "🟠";
                            break;
                        case "completed":
                            statusIcon = "✅";
                            break;
                        default:
                            statusIcon = "📋";
                    }

                    String orderText = statusIcon + " ЗАКАЗ #" + obj.getInt("id") + "\n" +
                            "📍 " + obj.getString("start_address") + " → " + obj.getString("end_address");

                    // Добавляем имя клиента если есть
                    if (obj.has("client_name") && !obj.isNull("client_name")) {
                        orderText += "\n👤 " + obj.getString("client_name");
                    }

                    // Добавляем водителя если есть
                    if (obj.has("driver_name") && !obj.isNull("driver_name") && !obj.getString("driver_name").isEmpty()) {
                        orderText += " | 🚗 " + obj.getString("driver_name");
                    }

                    ordersList.add(orderText);
                }

                runOnUiThread(() -> {
                    ordersAdapter.notifyDataSetChanged();
                    if (ridesData.isEmpty()) {
                        String message;
                        switch (currentStatus) {
                            case "new":
                                message = "Нет новых заказов";
                                break;
                            case "assigned":
                                message = "Нет назначенных заказов";
                                break;
                            case "in_progress":
                                message = "Нет заказов в пути";
                                break;
                            case "completed":
                                message = "Нет выполненных заказов";
                                break;
                            default:
                                message = "Нет заказов";
                        }
                        Toast.makeText(MainActivity.this, message, Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(MainActivity.this, "Заказов: " + ridesData.size(), Toast.LENGTH_SHORT).show();
                    }
                    refreshButton.setEnabled(true);
                    refreshButton.setText("🔄 Обновить заказы");
                });

            } catch (Exception e) {
                e.printStackTrace();
                runOnUiThread(() -> {
                    Toast.makeText(MainActivity.this, "Ошибка: " + e.getMessage(), Toast.LENGTH_SHORT).show();
                    refreshButton.setEnabled(true);
                    refreshButton.setText("🔄 Обновить заказы");
                });
            }
        });
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (executorService != null) {
            executorService.shutdown();
        }
    }
}
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:template match="/">
        <html>
            <head>
                <meta charset="UTF-8"/>
                <title>SNTF - نظام الرحلات</title>
                <style>
                    * {
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }
                    
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: #f5f5f5;
                        padding: 20px;
                    }
                    
                    .container {
                        max-width: 1600px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 8px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        overflow: hidden;
                    }
                    
                    /* Header */
                    .header {
                        background: #2c3e50;
                        color: white;
                        padding: 20px 25px;
                        border-bottom: 3px solid #3498db;
                    }
                    
                    .header h1 {
                        font-size: 24px;
                        margin-bottom: 5px;
                    }
                    
                    .header p {
                        font-size: 13px;
                        opacity: 0.8;
                    }
                    
                    /* Stats Section */
                    .stats-section {
                        background: #ecf0f1;
                        padding: 15px 25px;
                        border-bottom: 1px solid #ddd;
                    }
                    
                    .stats-table {
                        width: 100%;
                        background: white;
                        border-collapse: collapse;
                    }
                    
                    .stats-table td {
                        padding: 12px 15px;
                        text-align: center;
                        border: 1px solid #ddd;
                    }
                    
                    .stats-label {
                        font-weight: bold;
                        color: #2c3e50;
                        background: #f8f9fa;
                    }
                    
                    .stats-value {
                        font-size: 24px;
                        font-weight: bold;
                        color: #3498db;
                    }
                    
                    /* Main Table */
                    .data-table {
                        width: 100%;
                        border-collapse: collapse;
                    }
                    
                    .data-table th {
                        background: #34495e;
                        color: white;
                        padding: 12px 8px;
                        text-align: center;
                        font-size: 13px;
                        font-weight: 600;
                        border: 1px solid #46607a;
                    }
                    
                    .data-table td {
                        padding: 10px 8px;
                        text-align: center;
                        font-size: 13px;
                        border: 1px solid #ddd;
                    }
                    
                    .data-table tbody tr:hover {
                        background: #f0f7ff;
                    }
                    
                    /* Table cell colors */
                    .trip-code {
                        font-weight: bold;
                        color: #2c3e50;
                        font-family: 'Courier New', monospace;
                    }
                    
                    .train-normal {
                        background: #e8f4fd;
                        color: #2196f3;
                        font-weight: bold;
                        padding: 3px 8px;
                        border-radius: 3px;
                        display: inline-block;
                    }
                    
                    .train-rapid {
                        background: #fff3e0;
                        color: #ff9800;
                        font-weight: bold;
                        padding: 3px 8px;
                        border-radius: 3px;
                        display: inline-block;
                    }
                    
                    .train-coradia {
                        background: #e8f5e9;
                        color: #4caf50;
                        font-weight: bold;
                        padding: 3px 8px;
                        border-radius: 3px;
                        display: inline-block;
                    }
                    
                    .train-express {
                        background: #fce4ec;
                        color: #e91e63;
                        font-weight: bold;
                        padding: 3px 8px;
                        border-radius: 3px;
                        display: inline-block;
                    }
                    
                    .price {
                        color: #27ae60;
                        font-weight: bold;
                    }
                    
                    .class-economy {
                        color: #2980b9;
                        font-weight: 500;
                    }
                    
                    .class-vip {
                        color: #e74c3c;
                        font-weight: bold;
                    }
                    
                    .days {
                        font-size: 11px;
                        color: #7f8c8d;
                    }
                    
                    /* Footer */
                    .footer {
                        background: #2c3e50;
                        color: white;
                        text-align: center;
                        padding: 15px;
                        font-size: 12px;
                    }
                    
                    /* Scroll for table */
                    .table-wrapper {
                        overflow-x: auto;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <!-- Header -->
                    <div class="header">
                        <h1>🚆 الشركة الوطنية للنقل بالسكك الحديدية</h1>
                        <p>SNTF - نظام معلومات الرحلات</p>
                    </div>
                    
                    <!-- Statistics Table -->
                    <div class="stats-section">
                        <table class="stats-table">
                            <tr>
                                <td class="stats-label">📊 عدد الخطوط</td>
                                <td class="stats-value"><xsl:value-of select="count(transport/lines/line)"/></td>
                                <td class="stats-label">🚆 عدد الرحلات</td>
                                <td class="stats-value"><xsl:value-of select="count(transport/lines/line/trips/trip)"/></td>
                                <td class="stats-label">🏙️ عدد المحطات</td>
                                <td class="stats-value"><xsl:value-of select="count(transport/stations/station)"/></td>
                                <td class="stats-label">💺 عدد الدرجات</td>
                                <td class="stats-value"><xsl:value-of select="count(transport/lines/line/trips/trip/class)"/></td>
                            </tr>
                        </table>
                    </div>
                    
                    <!-- Main Data Table -->
                    <div class="table-wrapper">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>رمز الرحلة</th>
                                    <th>نوع القطار</th>
                                    <th>محطة المغادرة</th>
                                    <th>محطة الوصول</th>
                                    <th>وقت المغادرة</th>
                                    <th>وقت الوصول</th>
                                    <th>المدة</th>
                                    <th>الدرجة</th>
                                    <th>السعر (DZD)</th>
                                    <th>أيام السفر</th>
                                </tr>
                            </thead>
                            <tbody>
                                <xsl:for-each select="transport/lines/line">
                                    <xsl:variable name="departure_id" select="@departure"/>
                                    <xsl:variable name="arrival_id" select="@arrival"/>
                                    
                                    <xsl:for-each select="trips/trip">
                                        <xsl:variable name="trip_code" select="@code"/>
                                        <xsl:variable name="train_type" select="@type"/>
                                        <xsl:variable name="train_class">
                                            <xsl:choose>
                                                <xsl:when test="$train_type='Normal'">normal</xsl:when>
                                                <xsl:when test="$train_type='Rapid'">rapid</xsl:when>
                                                <xsl:when test="$train_type='Coradia'">coradia</xsl:when>
                                                <xsl:when test="$train_type='Express'">express</xsl:when>
                                                <xsl:otherwise>normal</xsl:otherwise>
                                            </xsl:choose>
                                        </xsl:variable>
                                        
                                        <xsl:for-each select="class">
                                            <xsl:variable name="class_type" select="@type"/>
                                            <xsl:variable name="price" select="@price"/>
                                            
                                            <!-- Calculate duration -->
                                            <xsl:variable name="dep_time" select="../schedule/@departure"/>
                                            <xsl:variable name="arr_time" select="../schedule/@arrival"/>
                                            
                                            <xsl:variable name="dep_hour" select="substring-before($dep_time, ':')"/>
                                            <xsl:variable name="dep_min" select="substring-after($dep_time, ':')"/>
                                            <xsl:variable name="arr_hour" select="substring-before($arr_time, ':')"/>
                                            <xsl:variable name="arr_min" select="substring-after($arr_time, ':')"/>
                                            
                                            <tr>
                                                <td><xsl:value-of select="position()"/></td>
                                                <td class="trip-code"><xsl:value-of select="$trip_code"/></td>
                                                <td>
                                                    <span class="train-{$train_class}">
                                                        <xsl:value-of select="$train_type"/>
                                                    </span>
                                                </td>
                                                <td><xsl:value-of select="//station[@id=$departure_id]/@name"/></td>
                                                <td><xsl:value-of select="//station[@id=$arrival_id]/@name"/></td>
                                                <td><xsl:value-of select="$dep_time"/></td>
                                                <td><xsl:value-of select="$arr_time"/></td>
                                                <td>
                                                    <xsl:value-of select="number($arr_hour) - number($dep_hour)"/>h
                                                    <xsl:value-of select="number($arr_min) - number($dep_min)"/>m
                                                </td>
                                                <td class="class-{translate($class_type, 'VIP', 'vip')}">
                                                    <xsl:value-of select="$class_type"/>
                                                </td>
                                                <td class="price"><xsl:value-of select="$price"/> DA</td>
                                                <td class="days"><xsl:value-of select="../days"/></td>
                                            </tr>
                                        </xsl:for-each>
                                    </xsl:for-each>
                                </xsl:for-each>
                            </tbody>
                        </table>
                    </div>
                    
                    <!-- Footer -->
                    <div class="footer">
                        © 2026 SNTF - جميع الحقوق محفوظة | تم إنشاء التقرير بواسطة نظام XSLT
                    </div>
                </div>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>
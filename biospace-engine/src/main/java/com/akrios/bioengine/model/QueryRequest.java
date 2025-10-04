package com.akrios.bioengine.model;

import java.util.Map;

public class QueryRequest {
    private String query;
    private String profile = "scientist"; // scientist | manager | architect
    private int k = 20;
    private Map<String, Object> filters;

    public QueryRequest() {}

    public String getQuery() { return query; }
    public void setQuery(String query) { this.query = query; }
    public String getProfile() { return profile; }
    public void setProfile(String profile) { this.profile = profile; }
    public int getK() { return k; }
    public void setK(int k) { this.k = k; }
    public Map<String, Object> getFilters() { return filters; }
    public void setFilters(Map<String, Object> filters) { this.filters = filters; }
}
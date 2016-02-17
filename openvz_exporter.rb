#!/opt/rbenv/shims/ruby

require 'sinatra'
require 'json'

set :bind, '::0'
set :port, 9119

class OpenVZPrometheus
  def vzlist
    JSON.parse(`vzlist -a -o hostname,ip,laverage -j`)
  end

  def to_prometheus(hostname, ip, value)
    "node_openvz_laverage{hostname=\"#{hostname}\", ip=\"#{ip}\"} #{value}\n"
  end

  def metrics
    vzlist.map do |vz|
      to_prometheus(vz['hostname'], vz['ip'].first, vz['laverage'].first)
    end
  end
end

get '/metrics' do
  content_type 'text/plain'
  OpenVZPrometheus.new.metrics
end

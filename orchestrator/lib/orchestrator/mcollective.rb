require 'mcollective'

module Orchestrator
  class MClient
    include MCollective::RPC
    include ::Orchestrator

    def initialize(task_id, agent, nodes=nil)
      @task_id = task_id
      @agent = agent
      @mc = rpcclient(agent)
      @mc.progress = false
      unless nodes.nil?
        @mc.discover(:nodes => nodes)
      end
    end

    def method_missing(method, *args)
      res = @mc.send(method, *args)
      unless method == :discover
        check_mcollective_result(method, res)
      end
      return res
    end

    private
    def check_mcollective_result(method, stats)
      # Following error might happen because of misconfiguration, ex. direct_addressing = 1 only on client
      raise "#{@task_id}: MCollective client failed to call agent '#{@agent}' with method '#{method}' and didn't even return anything. Check logs." if stats.length == 0
      stats.each do |node|
        status = node.results[:statuscode]
        if status != 0
          raise "#{@task_id}: MCollective call failed in agent '#{node.agent}', method '#{method}', results: #{node.results.inspect}"
        else
          ::Orchestrator.logger.debug "#{@task_id}: MC agent '#{node.agent}', method '#{method}' succeeded, results: #{node.results.inspect}"
        end
      end
    end
  end

end

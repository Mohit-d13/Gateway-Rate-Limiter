# Token bucket implementation using Redis Lua scripting.
# This script does the read-modify-write cycle in a single atomic operation.

BUCKET_SCRIPT = """
    local key         = KEYS[1]
    local capacity    = tonumber(ARGV[1])
    local refill_rate = tonumber(ARGV[2])
    local now         = tonumber(ARGV[3])

    -- Get value of last refill time and tokens from current state
    -- Parse it into variables
    local vals          = redis.call('HMGET', key, 'tokens', 'last_refill')
    local tokens        = tonumber(vals[1])
    local last_refill   = tonumber(vals[2])
    
    -- First request: initialize a full bucket
    if last_refill == nil then
        last_refill = now
        tokens = capacity
    end

    -- Refill calculation based on elapsed time and refill rate
    local elapsed     = now - last_refill
    local new_tokens  = math.min(capacity, tokens + (elapsed * refill_rate))

    -- Consume or deny
    if new_tokens < 1 then
        return {0, new_tokens}   -- denied, remaining
    end

    new_tokens = new_tokens - 1
    redis.call('HSET', key, 'tokens', new_tokens, 'last_refill', now)
    return {1, new_tokens}       -- allowed, remaining
    """

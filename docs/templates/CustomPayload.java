package com.example.network;

import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.chat.Component;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.neoforge.network.handling.IPayloadContext;

// 自定义网络包模板（客户端 → 服务端）
//
// 用法：
//   1. 复制本文件并重命名类与字段
//   2. 在 @Mod 构造函数中通过 RegisterPayloadHandlersEvent 注册
//   3. 客户端发送：minecraft.getConnection().send(new MyPayload(...))
public record MyPayload(int data, String label) implements CustomPacketPayload
{
    public static final Type<MyPayload> TYPE =
            new Type<>(Identifier.fromNamespaceAndPath("modid", "channel"));

    public static final StreamCodec<RegistryFriendlyByteBuf, MyPayload> STREAM_CODEC =
            StreamCodec.composite(
                    ByteBufCodecs.VAR_INT, MyPayload::data,
                    ByteBufCodecs.STRING_UTF8, MyPayload::label,
                    MyPayload::new);

    @Override
    public Type<MyPayload> type()
    {
        return TYPE;
    }

    // 服务端处理入口（enqueueWork 切主线程后执行）
    public static void handle(MyPayload payload, IPayloadContext ctx)
    {
        ctx.enqueueWork(() ->
        {
            if (!(ctx.player() instanceof ServerPlayer sp)) return;
            sp.sendSystemMessage(Component.literal("Got: " + payload.data + " " + payload.label));
        });
    }
}
